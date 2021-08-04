from abc import ABC, abstractmethod
from dataclasses import dataclass, Field as DCField
from inspect import isfunction
from typing import Callable, TypeVar, Generic, Tuple, final, Type, List, Optional

from dataclass_factory_30.common import TypeHint


@dataclass(frozen=True)
class ProvisionCtx:
    type: TypeHint


@dataclass
class CannotProvide(Exception):
    description: Optional[str] = None


class NoSuitableProvider(ValueError):
    pass


T = TypeVar('T')
V = TypeVar('V')
ProviderTV = TypeVar('ProviderTV', bound='Provider')


def _make_pipeline(left, right) -> 'Pipeline':
    if isinstance(left, Pipeline):
        left_elems = left.elements
    else:
        left_elems = (left,)

    if isinstance(right, Pipeline):
        right_elems = right.elements
    else:
        right_elems = (right,)

    return Pipeline(
        left_elems + right_elems
    )


class PipeliningMixin:
    """
    A mixin that makes your class able to create a pipeline
    """

    @final
    def __or__(self, other) -> 'Pipeline':
        return _make_pipeline(self, other)

    @final
    def __ror__(self, other) -> 'Pipeline':
        return _make_pipeline(other, self)


def provision_action(func: Callable[[ProviderTV, 'BaseFactory', int, ProvisionCtx], T]):
    """
    Marks method as provision_action.

    See :class:`Provider` for details.
    """
    func._is_provision_action = True  # type: ignore
    return func


def _get_provider_tmpl_pam(cls: 'Type[Provider[T]]') -> str:
    try:
        pam = cls._provision_action_method  # type: ignore
    except AttributeError:
        raise ValueError(f'{cls} has no defined provision action')

    if pam is None:
        raise ValueError(f'{cls} has several provision action')

    return pam


class Provider(PipeliningMixin, Generic[T], ABC):
    """Provider is a central part of core API.
    It takes information about a searched target and returns the expected instance.
    For example, :class:`ParserProvider` returns parser,
    :class:`NameMappingProvider` returns a new name of a field or None
    if this field must be omitted.

    If you want to apply provider you have to use only :method:`provide`.

    You can define ProviderTemplate if you mark one of the methods by @provision_action.
    The marked method will be used by :method:`provide` if you pass this class to provider_tmpl argument.

    The class can define only one @provision_action.
    You can not define a new @provision_action if the parent class has already defined one.

    So, if a class has only one method in MRO marked as @provision_action it is a ProviderTemplate.

    Provision action should be private and must be never called directly.

    Provider subclass can mix several ProviderTemplate and redefine its provision actions, but
    such class can not act as ProviderTemplate.

    Any provision action must return the expected value otherwise raise :exception:`CannotProvide`.

    Also, a provider can redefine :method:`_provide_other`.
    It is called if the main method has raised :exception:`CannotProvide`
    By default, it always raises CannotProvide
    """

    def __init_subclass__(cls, **kwargs):
        provision_action_list = [
            name for name, attr in vars(cls).items()
            if isfunction(attr) and getattr(attr, '_is_provision_action', False)
        ]

        if len(provision_action_list) > 1:
            raise ValueError('Class can not define several @provision_action')

        parents_pam_count = [
            '_provision_action_method' in vars(parent) for parent in cls.mro()
        ].count(True)

        if len(provision_action_list) == 1:
            if parents_pam_count > 0:
                raise ValueError(
                    'You cannot define a @provision_action'
                    ' because parent has already defined it'
                )

            cls._provision_action_method = provision_action_list[0]
        else:
            if parents_pam_count > 1 and cls._provision_action_method is not None:
                cls._provision_action_method = None

    def _provide_other(
        self,
        provider_tmpl: 'Type[Provider[T]]',
        factory: 'BaseFactory',
        offset: int,
        ctx: ProvisionCtx
    ) -> T:
        """Dynamic provision action.
        See :class:`Provider` for details.
        """
        raise CannotProvide

    @final
    def provide(
        self,
        provider_tmpl: 'Type[Provider[T]]',
        factory: 'BaseFactory',
        offset: int,
        ctx: ProvisionCtx
    ) -> T:
        """Returns provision result or raises :exception:`CannotProvide`

        See :class:`Provider` for details.
        """
        attr_name = _get_provider_tmpl_pam(provider_tmpl)
        if isinstance(self, provider_tmpl):
            try:
                return getattr(self, attr_name)(factory, offset, ctx)
            except CannotProvide:
                pass

        return self._provide_other(provider_tmpl, factory, offset, ctx)


def _get_class_own_recipe(cls: type):
    if (
        issubclass(cls, BaseFactory)
        and 'recipe' in vars(cls)
        and not isinstance(cls.recipe, DCField)
    ):
        return cls.recipe
    return []


class BaseFactory(ABC):
    """Factory creates requested object using a recipe.

    The recipe is a list that consists of :class:`Provider` or objects
    that a factory could cast to Provider.

    When you call :method:`provide`, a factory look for a suitable provider in a full recipe.
    The Full recipe is a sum of instance recipe and class recipe in MRO.
    See :method:`provide` for details of this process.

    :method:`provide` is a low-level method. Subclasses should introduce own user-friendly methods
    like `.parser(type)` of :class:`ParserFactory` or `.json_schema()` of :class:`JsonSchemaFactory`
    """
    recipe: list

    @abstractmethod
    def ensure_provider(self, value) -> Provider:
        """Create :class:`Provider` instance from value
        This method is used by :method:`provide` to convert each item of full_recipe
        to provider.

        :raise ValueError: Con not create Provider from given object
        """
        raise NotImplementedError

    def _full_recipe(self) -> list:
        """

        :return: A
        """
        result = self.recipe.copy()
        for item in type(self).mro():
            result.extend(
                _get_class_own_recipe(item)
            )
        return result

    @final
    def provide(self, provider_tmpl: Type[Provider[T]], offset: int, ctx: ProvisionCtx) -> T:
        """Provide expected value. Suitable provider searching in Full recipe
         that obtained by :method:`_full_recipe`

        :param provider_tmpl: Provider Template. See :class:`Provider` for details
        :param offset: Offset in Full recipe where need to start the search.
                       If offset is greater than the length of Full recipe
                       the method will try no providers, stop search
                       and so raise :class:`ValueError`
        :param ctx: Extensible context of search
        :return: Provision result. The type determines by :param provider_tmpl:
        :raise NoSuitableProvider: There is no suitable provider in the Full recipe
        """
        full_recipe = self._full_recipe()
        for idx, item in enumerate(full_recipe[offset:], start=offset):
            provider = self.ensure_provider(item)
            try:
                return provider.provide(provider_tmpl, self, offset, ctx)
            except CannotProvide:
                pass
        raise NoSuitableProvider(f'{self} can not create provider for {ctx}')


class PipelineEvalMixin(ABC):
    """
    A special mixin for Provider Template that allows to eval pipeline.
    Subclass should implement :method:`eval_pipeline`
    """

    @classmethod
    @abstractmethod
    def eval_pipeline(
        cls,
        providers: List[Provider],
        factory: 'BaseFactory',
        offset: int,
        ctx: ProvisionCtx
    ):
        pass


@dataclass(frozen=True)
class Pipeline(Provider, PipeliningMixin, Generic[V]):
    elements: Tuple[V, ...]

    def _provide_other(
        self,
        provider_tmpl: 'Type[Provider[T]]',
        factory: 'BaseFactory',
        offset: int,
        ctx: ProvisionCtx
    ) -> T:
        if not issubclass(provider_tmpl, PipelineEvalMixin):
            raise CannotProvide

        providers = [factory.ensure_provider(el) for el in self.elements]

        return provider_tmpl.eval_pipeline(
            providers, factory, offset, ctx
        )
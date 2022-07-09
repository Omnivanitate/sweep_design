from abc import ABCMeta, abstractmethod, abstractstaticmethod
from typing import Any, Dict, Generic, Iterable, Optional, Set, TypeVar, Union

from ..abc_common_framer_grapher.controller import CommonController

Output = TypeVar("Output")
Figure = TypeVar("Figure")
Controller = TypeVar("Controller", bound=CommonController)
Checkbox = TypeVar("Checkbox")
Dropbown = TypeVar("Dropbown")


class CommonFrameMaker(Generic[Figure, Controller], metaclass=ABCMeta):
    @abstractstaticmethod
    def get_figure_frame(
        figure: Figure, frame_properties: Dict[str, Any]
    ) -> "CommonFigureFrame[Figure]":
        pass

    @abstractstaticmethod
    def get_dropdown_frame(
        frame_properties: Dict[str, Any], controller: Controller
    ) -> "CommonDropdownFrame":
        pass

    @abstractstaticmethod
    def get_checkbox_frame(
        frame_properties: Dict[str, Any], controller: Controller
    ) -> "CommonCheckBoxFrame":
        pass


class CommonFrame(Generic[Output, Controller], metaclass=ABCMeta):
    def __init__(self, output: Output = None, controller: Controller = None) -> None:
        self._output = output
        self._controller = controller

    @property
    def controller(self) -> Optional[Controller]:
        return self._controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        self._controller = controller

    def get_output(self) -> Output:
        return self._output

    @abstractmethod
    def h_add(self, other: "CommonFrame") -> "CommonFrame":
        pass

    @abstractmethod
    def v_add(self, other: "CommonFrame") -> "CommonFrame":
        pass


class CommonFigureFrame(CommonFrame, Generic[Figure]):
    def __init__(self, figure: Figure, output: Output) -> None:
        super().__init__(output)
        self._figure = figure

    def get_figure(self) -> Figure:
        return self._figure


class CommonCheckBoxFrame(CommonFrame, Generic[Checkbox]):
    def __init__(self, output: Checkbox, controller: Controller = None) -> None:
        super().__init__(output, controller)
        self._checkboxs: Dict[str, CommonCheckBox] = {}

    @abstractmethod
    def add_choise(
        self,
        choise: str,
        groups: Union[str, Iterable[str]],
        checkbox_properties: Dict[str, Any],
        controller: Controller,
    ) -> None:
        pass

    @abstractmethod
    def return_choise(self, choise: str) -> None:
        pass

    @abstractmethod
    def remove_choise(self, choise: str) -> None:
        pass

    def remove_choise_by_groups(self, groups: Set[str]) -> None:
        for name_checkbox, checkbox in self._checkboxs.items():
            if groups.issubset(checkbox.get_groups()):
                self.remove_choise(name_checkbox)

    def return_choise_by_groups(self, groups: Set[str]) -> None:
        for name_checkbox, checkbox in self._checkboxs.items():
            if groups.issubset(checkbox.get_groups()):
                self.return_choise(name_checkbox)

    def get_checkboxs(self) -> Dict[str, "CommonCheckBox"]:
        return self._checkboxs

    def set_choise_by_name(self, name: str, value: bool) -> None:
        self._checkboxs[name].set_select(value)

    def set_choise_by_groups(self, groups: Union[str, Set[str]], value: bool) -> None:
        for choise_box in self._checkboxs.values():
            if groups.issubset(choise_box.get_groups()):
                choise_box.set_select(value)


class CommonCheckBox(CommonFrame, Generic[Checkbox, Controller]):
    def __init__(
        self,
        checkbox: Checkbox,
        name: str,
        groups: Union[str, Iterable[str]],
        controller: Controller,
    ) -> None:

        super().__init__(checkbox, controller)
        self._name = name
        if isinstance(groups, str):
            groups = set([groups])
        elif groups is not None:
            self._groups = set(groups)
        else:
            self._groups = set()
        self._checkbox = checkbox

    def get_name(self) -> str:
        return self._name

    def get_groups(self) -> Set[str]:
        return self._groups

    @abstractmethod
    def set_select(self, value: bool) -> None:
        pass


class CommonDropdownFrame(CommonFrame, Generic[Dropbown]):
    def __init__(
        self, dropdown: Dropbown, no_data_name: str, controller: Controller = None
    ) -> None:
        super().__init__(dropdown, controller)
        self._no_data_name = no_data_name
        self._dropdown = dropdown

    @abstractmethod
    def add_choise(self, choise: str) -> None:
        pass

    @abstractmethod
    def remove_choise(self, choise: str) -> None:
        pass

    @abstractmethod
    def get_choise(self) -> str:
        pass

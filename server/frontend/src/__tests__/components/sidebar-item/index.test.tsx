import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { shallow } from "enzyme";

import { SidebarItem } from "components/sidebar-item";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    const label = "test_label";
    const icon = "test_icon";
    const path = "/";
    render(
      <BrowserRouter>
        <SidebarItem path={path} label={label} icon={icon} />
      </BrowserRouter>
    );
  });

  test("Passes down props", () => {
    const props = {
      label: "test_label",
      icon: "test_icon",
      path: "/",
      highlighted: true,
    };
    const wrapper = shallow(<SidebarItem {...props} />);
    expect(wrapper.find("SidebarItemView").props()).toStrictEqual(props);
  });
});

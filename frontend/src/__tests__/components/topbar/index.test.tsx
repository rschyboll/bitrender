import { render } from "@testing-library/react";

import { Topbar } from "components/topbar";
import { shallow } from "enzyme";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

jest.mock("react-router", () => ({
  useLocation: () => {
    return { pathname: "/machines" };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    render(<Topbar />);
  });

  test("Passes down current path name", () => {
    const wrapper = shallow(<Topbar />);
    expect(wrapper.find("TopbarView").props()).toStrictEqual({ pathName: "machines" });
  });
});

describe("Presentational tests", () => {});

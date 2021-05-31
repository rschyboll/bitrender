import { render, screen } from "@testing-library/react";
import { shallow } from "enzyme";

import { Logo } from "components/logo";

describe("Functional tests", () => {
  test("Renders without errors", () => {
    render(<Logo />);
    const logoElement = screen.getByRole("img");
    expect(logoElement).toBeInTheDocument();
  });
  test("Passes props to view", () => {
    render(<Logo />);
    const props = { className: "test", style: { color: "red" } };
    const wrapper = shallow(<Logo {...props} />);
    expect(wrapper.find("LogoView").props()).toStrictEqual(props);
  });
});

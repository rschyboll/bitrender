import { render, screen } from "@testing-library/react";

import { TopbarView } from "components/topbar/view";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    const pathName = "test";
    render(<TopbarView pathName={pathName} />);
  });
});

describe("Presentational tests", () => {
  test("Renders current path name", () => {
    const pathName = "test";
    render(<TopbarView pathName={pathName} />);
    const logoElement = screen.getByText("navigation." + pathName);
    expect(logoElement).toBeInTheDocument();
  });
});

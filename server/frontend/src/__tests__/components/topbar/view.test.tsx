import { render, screen } from "@testing-library/react";

import { TopbarView } from "../../../components/topbar/view";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

test("Renders without errors", () => {
  const location = "test";
  render(<TopbarView location={location} />);
  const logoElement = screen.getByText("navigation." + location);
  expect(logoElement).toBeInTheDocument();
});

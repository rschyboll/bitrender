import { render, screen } from "@testing-library/react";

import { LogoView } from "../../../components/logo/view";

test("Renders without errors", () => {
  render(<LogoView />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toBeInTheDocument();
});

test("Has src and alt attributes", () => {
  render(<LogoView />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toHaveAttribute("src", "logo.png");
  expect(logoElement).toHaveAttribute("alt", "logo");
});

test("Has class and style when providing props", () => {
  render(<LogoView className="test" style={{ backgroundColor: "red" }} />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toHaveClass("test");
  expect(logoElement).toHaveStyle("background-color: red");
});

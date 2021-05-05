import { render, screen } from "@testing-library/react";

import { Logo } from "../../../components/logo/logo";

test("Renders without errors", () => {
  render(<Logo />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toBeInTheDocument();
});

test("Has src and alt attributes", () => {
  render(<Logo />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toHaveAttribute("src", "logo.png");
  expect(logoElement).toHaveAttribute("alt", "logo");
});

test("Has class and style when providing props", () => {
  render(<Logo className="test" style={{ backgroundColor: "red" }} />);
  const logoElement = screen.getByRole("img");
  expect(logoElement).toHaveClass("test");
  expect(logoElement).toHaveStyle("background-color: red");
});

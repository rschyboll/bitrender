import { fireEvent, render, screen } from "@testing-library/react";
import { BrowserRouter, Router } from "react-router-dom";
import { createMemoryHistory } from "history";

import { SidebarItemView } from "../../../components/sidebar-item/view";

jest.mock("primereact/button", () => {
  return {
    Button: (props: { className: string; label: string; icon: string }) => {
      return <button className={props.className}>{props.label + " " + props.icon}</button>;
    },
  };
});

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

test("Renders without errors", () => {
  const label = "test_label";
  const icon = "test_icon";
  const path = "/";
  render(
    <BrowserRouter>
      <SidebarItemView path={path} label={label} icon={icon} />
    </BrowserRouter>
  );
});

test("Changes path on click", () => {
  const history = createMemoryHistory();
  const label = "test_label";
  const icon = "test_icon";
  const path = "/test";
  render(
    <Router history={history}>
      <SidebarItemView path={path} label={label} icon={icon} />
    </Router>
  );
  const buttonElement = screen.getByRole("button");
  expect(history.location.pathname).toBe("/");
  fireEvent(buttonElement, new MouseEvent("click", { bubbles: true, cancelable: true }));
  expect(history.location.pathname).toBe("/test");
});

test("Has correct output", () => {
  const label = "test_label";
  const icon = "test_icon";
  const path = "/";
  render(
    <BrowserRouter>
      <SidebarItemView path={path} label={label} icon={icon} />
    </BrowserRouter>
  );
  const buttonElement = screen.getByRole("button");
  expect(buttonElement).toHaveTextContent(label + " " + icon);
});

test("Throws exception when not in router", () => {
  const label = "test_label";
  const icon = "test_icon";
  const path = "/";
  console.error = () => {};
  expect(() => render(<SidebarItemView path={path} label={label} icon={icon} />)).toThrow();
});

test("Changes color on right path", () => {
  const label = "test_label";
  const icon = "test_icon";
  const path = "/";
  render(
    <BrowserRouter>
      <SidebarItemView path={path} label={label} icon={icon} highlighted={true} />
    </BrowserRouter>
  );
  const linkElement = screen.getByRole("button").parentElement;
  expect(linkElement).toHaveClass("sidebar-item-highlighted");
});

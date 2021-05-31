import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { SidebarView } from "components/sidebar/view";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    const items = [
      { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/" },
      { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
      { label: "navigation.machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
    ];
    render(
      <BrowserRouter>
        <SidebarView items={items} />
      </BrowserRouter>
    );
  });
});

describe("Presentational tests", () => {
  test("Renders children correctly", () => {
    const items = [
      { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/" },
      { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
      { label: "navigation.machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
    ];
    render(
      <BrowserRouter>
        <SidebarView items={items} />
      </BrowserRouter>
    );

    const sidebar = screen.getByRole("navigation");
    expect(sidebar).toBeInTheDocument();

    const buttons = screen.getAllByRole("button");
    expect(buttons.length).toBe(3);

    items.forEach((item) => {
      const button = screen.getByText(item.label);
      expect(button).toBeInTheDocument();
    });
  });
  test("Renders current path correctly", () => {
    const items = [
      { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/", highlighted: true },
      { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
      { label: "navigation.machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
    ];
    render(
      <BrowserRouter>
        <SidebarView items={items} />
      </BrowserRouter>
    );
    const button = screen.getByText(items[0].label);
    expect(button.parentElement?.parentElement?.className).toContain("highlighted");
  });
});

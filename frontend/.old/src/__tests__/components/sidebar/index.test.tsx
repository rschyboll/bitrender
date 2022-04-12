import { render } from "@testing-library/react";
import { Router, BrowserRouter } from "react-router-dom";
import { mount } from "enzyme";
import { createMemoryHistory } from "history";

import { Sidebar } from "components/sidebar";
import { SidebarViewProps } from "components/sidebar/view";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    render(
      <BrowserRouter>
        <Sidebar />
      </BrowserRouter>
    );
  });

  test("Highlights correct path", () => {
    const history = createMemoryHistory();
    const wrapper = mount(
      <Router history={history}>
        <Sidebar />
      </Router>
    );
    expect(history.location.pathname).toBe("/");
    const props = wrapper.find("SidebarView").props() as SidebarViewProps;
    for (const item of props.items) {
      expect(item.highlighted).toBe(item.path === history.location.pathname);
    }
  });
});

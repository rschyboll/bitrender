import { highlightCurrentPath } from "components/sidebar/logic";

describe("Functional tests", () => {
  test("Highlights correct path", () => {
    const items = [
      { label: "test_label", icon: "test_icon", path: "/" },
      { label: "test_label2", icon: "test_icon2", path: "/test" },
    ];
    const newItems = highlightCurrentPath(items, "/");
    expect(newItems[0].highlighted).toBe(true);
    expect(newItems[1].highlighted).toBe(false);
  });

  test("Does not return the same object", () => {
    const items = [
      { label: "test_label", icon: "test_icon", path: "/" },
      { label: "test_label2", icon: "test_icon2", path: "/test" },
    ];
    const newItems = highlightCurrentPath(items, "/");
    expect(items === newItems).toBe(false);
  });
});

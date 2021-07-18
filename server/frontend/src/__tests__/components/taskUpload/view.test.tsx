import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { TaskUploadView } from "components/taskUpload/view";
import React from "react";
import { act } from "react-dom/test-utils";

function mockData(files: File[]) {
  return {
    dataTransfer: {
      files,
      items: files.map((file) => ({
        kind: "file",
        type: file.type,
        getAsFile: () => file,
      })),
      types: ["Files"],
    },
  };
}
function dispatchEvt(node: Element, type: string, data: Object) {
  const event = new Event(type, { bubbles: true });
  Object.assign(event, data);
  fireEvent(node, event);
}

async function flushPromises(
  rerender: (ui: React.ReactElement<any, string | React.JSXElementConstructor<any>>) => void,
  ui: React.ReactElement<any, string | React.JSXElementConstructor<any>>
) {
  await act(() => waitFor(() => rerender(ui)));
}

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    const messagesRef = { current: null };
    const onDropAccepted = jest.fn();
    const onDropRejected = jest.fn();
    render(
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );
  });
  test("Calls onDropAccepted when dropping .blend file", async () => {
    const messagesRef = { current: null };
    const onDropRejected = jest.fn();
    const onDropAccepted = jest.fn();

    const file = new File(["test"], "test.blend");
    const data = mockData([file]);

    const ui = (
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );

    const { container, rerender } = render(ui);
    const section = container.querySelector("section") as Element;

    dispatchEvt(section, "drop", data);
    await flushPromises(rerender, ui);

    expect(onDropAccepted).toHaveBeenCalledWith([file], expect.any(Object));
  });
  test("Calls onDropRejected when dropping wrong file", async () => {
    const messagesRef = { current: null };
    const onDropAccepted = jest.fn();
    const onDropRejected = jest.fn();

    const file = new File(["test"], "test.png");
    const data = mockData([file]);

    const ui = (
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );

    const { container, rerender } = render(ui);
    const section = container.querySelector("section") as Element;

    dispatchEvt(section, "drop", data);
    await flushPromises(rerender, ui);

    expect(onDropRejected).toHaveBeenCalledWith([{ file: file, errors: expect.any(Object) }], expect.any(Object));
  });

  test("Accepts only one file", async () => {
    const messagesRef = { current: null };
    const onDropAccepted = jest.fn();
    const onDropRejected = jest.fn();

    let files = [new File(["test"], "test.blend"), new File(["test2"], "test2.blend")];
    let data = mockData(files);

    const ui = (
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );
    const { container, rerender } = render(ui);
    const section = container.querySelector("section") as Element;

    dispatchEvt(section, "drop", data);
    await flushPromises(rerender, ui);

    expect(onDropRejected).toHaveBeenCalled();

    files = [new File(["test"], "test.blend")];
    data = mockData(files);

    dispatchEvt(section, "drop", data);
    await flushPromises(rerender, ui);

    expect(onDropAccepted).toHaveBeenCalled();
  });
});

describe("Presentational tests", () => {
  test("Renders svg logo", () => {
    const messagesRef = { current: null };
    const onDropAccepted = jest.fn();
    const onDropRejected = jest.fn();
    render(
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );
    const img = screen.getByRole("img");
    expect(img).toBeInTheDocument();
  });
  test("Renders outline when dropping file", async () => {
    const messagesRef = { current: null };
    const onDropAccepted = jest.fn();
    const onDropRejected = jest.fn();

    const file = new File(["test"], "test.blend");
    const data = mockData([file]);

    const ui = (
      <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />
    );

    const { container, rerender } = render(ui);
    const section = container.querySelector("section") as Element;

    expect(section.className).not.toContain("focus");

    dispatchEvt(section, "dragenter", data);
    await flushPromises(rerender, ui);

    expect(section.className).toContain("focus");
  });
});

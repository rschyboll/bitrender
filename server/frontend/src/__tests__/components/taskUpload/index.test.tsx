import { render } from "@testing-library/react";
import { shallow } from "enzyme";

import { TaskUpload } from "components/taskUpload";

jest.mock("react-i18next", () => ({
  useTranslation: () => {
    return {
      t: (str: string) => str,
    };
  },
}));

describe("Functional tests", () => {
  test("Renders without errors", () => {
    const setFile = (file: File | undefined) => {};
    const file: File | undefined = undefined;
    render(<TaskUpload setFile={setFile} file={file} />);
  });
});

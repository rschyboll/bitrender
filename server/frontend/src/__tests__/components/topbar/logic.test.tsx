import { getPathName } from "components/topbar/logic";

describe("Functional tests", () => {
  test("Returns correct pathName for /machines", () => {
    const location = { pathname: "/machines" };
    const pathName = getPathName(location);
    expect(pathName).toBe("machines");
  });
  test("Returns correct pathName for /", () => {
    const location = { pathname: "/" };
    const pathName = getPathName(location);
    expect(pathName).toBe("dashboard");
  });
});

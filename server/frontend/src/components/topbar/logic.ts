export function getPathName(location: { pathname: string }) {
  const pathName = location.pathname.replace("/", "");

  if (pathName === "") {
    return "dashboard";
  }
  return pathName;
}

export function getFileSizeInMB(size: number): String {
  return (size / 1024 / 1024).toFixed(1) + "MB";
}

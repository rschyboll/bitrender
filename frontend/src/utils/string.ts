/**
 * Capitalizes the first letter of a string.
 *
 * This function converts the first letter of the input string to uppercase using the rules of the specified locale.
 * If the input string is empty, then an empty string is returned.
 *
 * @param str - The string to capitalize.
 * @returns The input string with the first letter capitalized.
 */
export function capitalizeFirstLetter(str: string): string {
  if (str.length === 0) {
    return '';
  }
  return str.charAt(0).toLocaleUpperCase() + str.slice(1);
}

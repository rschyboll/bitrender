function getCssBreakpoints(): {
  mobile: string;
  tablet: string;
  dekstop: string;
} {
  return Object.fromEntries(
    Object.entries(config.breakpoints).map((entry) => {
      return [entry[0], entry[1].toString() + 'px'];
    }),
  ) as {
    mobile: string;
    tablet: string;
    dekstop: string;
  };
}

const config = {
  breakpoints: {
    mobile: 480,
    tablet: 768,
    desktop: 1024,
  },
  get cssBreakpoints() {
    return getCssBreakpoints();
  },
};

console.log(config.cssBreakpoints);

export default config;

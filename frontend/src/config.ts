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
  loadDelay: 100,
  dataCleanTimeout: 5000,
  containerUnmountDelay: 1000,
  breakpoints: {
    mobile: 480,
    tablet: 768,
    desktop: 1024,
  },
  get cssBreakpoints() {
    return getCssBreakpoints();
  },
};

export default config;

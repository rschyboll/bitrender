module.exports = {
  presets: [
    [
      '@babel/preset-react',
      {
        runtime: 'automatic',
        development: process.env.NODE_ENV === 'development',
        importSource: '@welldone-software/why-did-you-render',
      },
    ],
  ],
  plugins: [['@babel/plugin-proposal-decorators', { version: 'legacy' }]],
};

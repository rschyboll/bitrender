import { resetContext } from 'kea';
import { localStoragePlugin } from 'kea-localstorage';
import { routerPlugin } from 'kea-router';

resetContext({
  plugins: [localStoragePlugin, routerPlugin({})],
});

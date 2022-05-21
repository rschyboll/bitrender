import { resetContext } from 'kea';
import { localStoragePlugin } from 'kea-localstorage';

resetContext({
  plugins: [localStoragePlugin],
});

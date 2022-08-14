import whyDidYouRender from '@welldone-software/why-did-you-render';
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  whyDidYouRender(React, {
    trackAllPureComponents: true,
    logOnDifferentValues: true,
    logOwnerReasons: true,
    trackHooks: true,
  });
}

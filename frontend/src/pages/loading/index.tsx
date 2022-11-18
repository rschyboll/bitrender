import { Button } from 'primereact/button';
import { memo, useState } from 'react';
import { Trans } from 'react-i18next';

import { Dialog } from '@/components/dialog';

import './style.scss';

export const LoadingPage = memo(function LoadingPage() {
  const [visible, setVisible] = useState(false);

  return (
    <>
      <Button
        className="delete-button p-button-danger"
        tooltip={'role.deleteButtonTooltip'}
        label="TEST"
        tooltipOptions={{ showDelay: 1000, position: 'top' }}
        onClick={() => setVisible(!visible)}
      />
      <Dialog visible={visible}>Test</Dialog>
    </>
  );
});

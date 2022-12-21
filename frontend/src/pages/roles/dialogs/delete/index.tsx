import { Localized } from '@fluent/react';
import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Skeleton } from 'primereact/skeleton';
import { VirtualScrollerLazyParams } from 'primereact/virtualscroller';
import { memo, useCallback, useMemo, useRef, useState } from 'react';

import { Dialog } from '@/components/dialog';
import { Dropdown } from '@/components/dropdown';
import ResponseHandler from '@/components/responseHandler';
import { useOptionalValues } from '@/logic/hooks';
import { IRoleDeleteLogic } from '@/logic/interfaces';
import { IRoleVirtualLoaderLogic } from '@/logic/interfaces/roles/loaders/virtual';
import { RequestStatus } from '@/services';

import styles from './style.module.scss';
import './translations';

export type DeleteRoleDialogProps = {
  id: string;
  visible: boolean;
  setVisible: (visible: boolean) => void;
};

export const DeleteRoleDialog = memo(function DeleteRoleDialog(
  props: DeleteRoleDialogProps,
) {
  const removeRoleLogic = useInjection(IRoleDeleteLogic.$)({ id: props.id });

  const { viewLoadStatus } = useOptionalValues(removeRoleLogic);

  const onDialogClose = useCallback(() => {
    props.setVisible(false);
  }, [props.setVisible]);

  return (
    <>
      <Localized
        id="deleteRoleDialog"
        attrs={{ title: true, acceptLabel: true }}
      >
        <Dialog
          onHide={onDialogClose}
          onAccept={() => {}}
          visible={props.visible}
        >
          <Localized id="deleteRoleDialogBody" attrs={{ translations: true }}>
            <Body id={props.id} />
          </Localized>
        </Dialog>
      </Localized>
    </>
  );
});

interface BodyProps {
  id: string;
  titleMessage?: string;
  userCountMessage?: string;
}

const Body = memo(function Body(props: BodyProps) {
  const roleDeleteLogic = useInjection(IRoleDeleteLogic.$)({ id: props.id });

  const {
    view,
    viewLoadStatus,
    viewLoadError,
    userCount,
    userCountLoadStatus,
    userCountLoadError,
  } = useValues(roleDeleteLogic);

  const [range, setRange] = useState<[number, number]>([0, 0]);

  const roleVirtualLoaderLogic = useInjection(IRoleVirtualLoaderLogic.$)({
    beginning: range[0],
    end: range[1],
    key: `DeleteRoleDialog:${props.id}`,
  });

  const { entries, entryCount, loadStatus } = useValues(roleVirtualLoaderLogic);

  const requestStatuses = useMemo(() => {
    return [
      { loaded: view != null, status: viewLoadStatus, error: viewLoadError },
      {
        loaded: userCount != null,
        status: userCountLoadStatus,
        error: userCountLoadError,
      },
    ];
  }, [
    userCount,
    userCountLoadError,
    userCountLoadStatus,
    view,
    viewLoadError,
    viewLoadStatus,
  ]);

  const onLazyLoad = useCallback(
    (params: VirtualScrollerLazyParams) => {
      console.log(params);
      if (params.last == 0) {
        return;
      }

      if (typeof params.first == 'number' && typeof params.last == 'number') {
        if (params.first != range[0] || params.last != range[1]) {
          setRange([params.first, params.last]);
        }
      }
    },
    [range],
  );

  return (
    <ResponseHandler requestStatuses={requestStatuses}>
      {props.titleMessage}
      {props.userCountMessage}
      {userCount != null ? (
        <Dropdown
          options={Object.values(entries).map((entry) => {
            if (entry == null) {
              return { notLoaded: true };
            }
            return entry.name;
          })}
          itemTemplate={(item) => {
            if (item['notLoaded'] === true) {
              return <Skeleton width={'60%'} height="1rem" />;
            }

            return item;
          }}
          showFilterClear
          filter
          onFilter={(e) => {
            console.log(e);
          }}
          virtualScrollerOptions={{
            lazy: true,
            onLazyLoad: onLazyLoad,
            itemSize: 30,
            loading: loadStatus == RequestStatus.Running,
            showLoader: true,
          }}
          placeholder="Select Item"
        />
      ) : null}
    </ResponseHandler>
  );
});

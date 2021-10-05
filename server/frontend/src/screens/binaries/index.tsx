import React, { FunctionComponent, useEffect, useState } from "react";
import { useDispatch } from "react-redux";

import { binariesSlice } from "store/binaries/reducer";
import { binariesSelectors } from "store/binaries/selectors";
import { FetchStatus } from "store/binaries/types";
import { BinariesView } from "./view";
import "./style.scss";

export type BinariesProps = {};

export const Binaries: FunctionComponent<BinariesProps> = () => {
  const dispatch = useDispatch();
  const binaries = binariesSelectors.useBinariesData();
  const fetchStatus = binariesSelectors.useBinariesFetchStatus();

  const [dialogVisible, setDialogVisible] = useState(false);

  useEffect(() => {
    dispatch(binariesSlice.actions.fetchStart());
  }, [dispatch]);

  const showDialog = (value: boolean) => {
    setDialogVisible(value);
  };

  const addNewBinary = (url: string, version: string) => {
    setDialogVisible(false);
    dispatch(
      binariesSlice.actions.addNewBinary({ url: url, version: version })
    );
  };

  const deleteBinary = (id: string) => {
    dispatch(binariesSlice.actions.deleteBinary({ id: id }));
  };

  return (
    <BinariesView
      loading={fetchStatus === FetchStatus.loading}
      binaries={binaries}
      dialogVisible={dialogVisible}
      showDialog={showDialog}
      addNewBinary={addNewBinary}
      deleteBinary={deleteBinary}
    />
  );
};

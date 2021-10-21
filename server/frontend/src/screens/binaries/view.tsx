import React, { FunctionComponent } from "react";
import { useTranslation } from "react-i18next";

import { PrimeIcons } from "primereact/api";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { BinariesDialog } from "./dialog";
import { BinaryData } from "store/binaries/types";

const TableHeader: FunctionComponent<{ showDialog: (arg0: boolean) => void }> =
  (props) => {
    const { t } = useTranslation();
    const onClick = () => props.showDialog(true);

    return (
      <Button
        onClick={onClick}
        icon={PrimeIcons.PLUS}
        label={t("binaries.new")}
      />
    );
  };

export type BinariesViewProps = {
  binaries: BinaryData[];
  loading: boolean;
  showDialog: (arg0: boolean) => void;
  dialogVisible: boolean;
  addNewBinary: (url: string, version: string) => void;
  deleteBinary: (id: string) => void;
};

export const BinariesView: FunctionComponent<BinariesViewProps> = (props) => {
  const { t } = useTranslation();

  const RemoveButton = (rowData: {
    version: string;
    url: string;
    id: string;
  }) => {
    return (
      <Button
        icon="pi pi-trash"
        className="p-button-rounded p-button-warning"
        onClick={() => props.deleteBinary(rowData.id)}
      />
    );
  };

  return (
    <>
      <Card>
        <DataTable
          header={<TableHeader showDialog={props.showDialog} />}
          value={props.binaries}
          loading={props.loading}
        >
          <Column field="version" header={t("binaries.version")} />
          <Column field="url" header={t("binaries.url")} />
          <Column body={RemoveButton} />
        </DataTable>
        <BinariesDialog
          dialogVisible={props.dialogVisible}
          showDialog={props.showDialog}
          addNewBinary={props.addNewBinary}
        />
      </Card>
    </>
  );
};

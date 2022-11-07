import { useInjection } from "inversify-react";
import { useActions, useValues } from "kea";
import { Button } from "primereact/button";
import { FC, useCallback, useState } from "react";
import { RiCloseFill } from "react-icons/ri";
import { IoAdd } from "react-icons/io5";
import { RiSearchLine } from "react-icons/ri";

import { Card, IconCard } from "@/components/card";
import { DataTable } from "@/components/dataTable";
import { TextField } from "@/components/textField";
import { IRolesTableLogic } from "@/logic/interfaces";
import { Dialog } from "primereact/dialog";

import { ModifyColumn } from "./columns/modify";
import "./style.scss";
import { rolesTableModel } from "./tableModel";
import { AddRoleDialog } from "./dialogs/add";

const RolesPage: FC = () => {
  return (
    <div className="roles-page grid">
      <IconCard
        className="roles-default-role-card col-12 desktop:col-6"
        title="Orders"
        color="#64B5F6"
        icon={RiSearchLine}
      >
        Test
      </IconCard>
      <IconCard
        className="roles-default-role-counter-card col-12 desktop:col-6"
        title="Orders"
        color="#64B5F6"
        icon={RiSearchLine}
      >
        Test
      </IconCard>
      <Card
        title="Lista roli użytkowników"
        titleActions={
          <>
            <TableSearchField />
            <TableAddButton />
          </>
        }
        className="roles-table-card col-12"
      >
        <DataTable
          logicIdentifier={IRolesTableLogic.$}
          model={rolesTableModel}
          customColumns={{
            after: {
              modify: {
                content: ModifyColumn,
              },
            },
          }}
        />
      </Card>
    </div>
  );
};

const TableSearchField = () => {
  const rolesTableLogic = useInjection(IRolesTableLogic.$);

  const { searchString } = useValues(rolesTableLogic);
  const { setSearchString } = useActions(rolesTableLogic);

  return (
    <TextField
      value={searchString != null ? searchString : ""}
      onChange={setSearchString}
      className="search-field"
      leftIcon={RiSearchLine}
      hasFloor={false}
      placeholder={"search"}
    />
  );
};

const TableAddButton = () => {
  const [dialogVisible, setDialogVisible] = useState(false);

  const onAddNewButtonClick = useCallback(
    () => setDialogVisible(!dialogVisible),
    [dialogVisible]
  );

  const onDialogDismiss = useCallback(() => setDialogVisible(false), []);

  const onDialogClose = useCallback(() => setDialogVisible(false), []);

  const icons = useCallback(() => {
    return (
      <Button
        className="p-button-text p-button-rounded p-button-plain"
        icon={<RiCloseFill />}
        onClick={onDialogClose}
      />
    );
  }, [onDialogClose]);

  return (
    <>
      <Button
        className="add-new-button"
        label={"Testt"}
        icon={<IoAdd size="1.75rem" />}
        onClick={onAddNewButtonClick}
      />
      <Dialog
        visible={dialogVisible}
        onHide={onDialogDismiss}
        icons={icons}
        dismissableMask
        closable={false}
      >
        <AddRoleDialog />
      </Dialog>
    </>
  );
};

export default RolesPage;

import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { PrimeIcons } from "primereact/api";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";
import { TaskData } from "store/tasks/types";
import { Column } from "primereact/column";

const TableHeader: FunctionComponent = () => {
  const { t } = useTranslation();

  return (
    <div>
      <Link className="link" to="/addTask">
        <Button icon={PrimeIcons.PLUS} label={t("tasks.new")} />
      </Link>
    </div>
  );
};

export type TasksViewProps = {
  tasks: TaskData[];
  deleteTask: (task: TaskData) => void;
};

export const TasksView: FunctionComponent<TasksViewProps> = (props) => {
  const { t } = useTranslation();

  const actionBodyTemplate = (rowData: TaskData) => {
    return (
      <Button
        icon="pi pi-trash"
        className="p-button-rounded p-button-warning"
        onClick={() => props.deleteTask(rowData)}
      />
    );
  };

  return (
    <Card>
      <DataTable stripedRows header={<TableHeader />} value={props.tasks}>
        <Column field="name" header={t("tasks.name")} />
        <Column field="samples" header={t("tasks.samples")} />
        <Column field="start_frame" header={t("tasks.start_frame")} />
        <Column field="end_frame" header={t("tasks.end_frame")} />
        <Column field="resolution_x" header={t("tasks.resolution_x")} />
        <Column field="resolution_y" header={t("tasks.resolution_y")} />
        <Column
          body={actionBodyTemplate}
          exportable={false}
          style={{ minWidth: "8rem" }}
        ></Column>
      </DataTable>
    </Card>
  );
};

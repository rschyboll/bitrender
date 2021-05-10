import { FunctionComponent } from "react";
import { PrimeIcons } from "primereact/api";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";

const TableHeader: FunctionComponent = () => {
  return (
    <div>
      <Button icon={PrimeIcons.PLUS} label="New" />
    </div>
  );
};

export type TasksViewProps = {};

export const TasksView: FunctionComponent<TasksViewProps> = () => {
  return (
    <Card>
      <DataTable header={<TableHeader />} />
    </Card>
  );
};

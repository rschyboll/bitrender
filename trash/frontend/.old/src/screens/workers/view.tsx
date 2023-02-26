import { FunctionComponent } from "react";

import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { WorkerData } from "store/workers/types";

export type WorkersViewProps = {
  activateWorker: (id: string) => void;
  workers: WorkerData[];
  loading: boolean;
};

export const WorkersView: FunctionComponent<WorkersViewProps> = (props) => {
  const parse_date = (date: string) => {
    let unix = Date.parse(date);
    let date_time = new Date(unix);

    var year = date_time.getFullYear();
    var month = date_time.getMonth();
    var day = date_time.getDate();
    var hour = date_time.getHours();
    var min = date_time.getMinutes();
    var sec = date_time.getSeconds();
    var time =
      day + "." + month + "." + year + " " + hour + ":" + min + ":" + sec;
    return time;
  };

  return (
    <div className="p-grid p-mt-2 mygrid">
      {props.workers.map((worker) => (
        <Card
          key={worker.id}
          style={{ display: "table" }}
          className="worker-box"
        >
          <h5>
            <i className="pi pi-th-large"></i>
            {" " + worker.name}
          </h5>
          <p>Zarejestrowany w: </p>
          <b> {parse_date(worker.create_date)}</b>
          <div className="spacer" />
          <div className="align-left">
            {worker.active ? (
              <Button label="Aktywny" disabled={true} />
            ) : (
              <Button
                label="Aktywuj"
                onClick={() => {
                  props.activateWorker(worker.id);
                }}
              />
            )}
          </div>
        </Card>
      ))}
    </div>
  );
};

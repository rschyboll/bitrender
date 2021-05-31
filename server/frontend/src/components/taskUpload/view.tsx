import { FunctionComponent } from "react";

import { FileUpload } from "primereact/fileupload";

export const TaskUploadView: FunctionComponent = () => {
  return (
    <FileUpload
      emptyTemplate={<p className="p-m-0">Drag and drop files to here to upload.</p>}
      accept=".blend"
      name="task"
      url="https://primefaces.org/primereact/showcase/upload.php"
      multiple
    />
  );
};

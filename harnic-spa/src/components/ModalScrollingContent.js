import React, { useState } from "react";

import { Modal } from "semantic-ui-react";


const ModalScrollingContent = ({ header, trigger, children }) => {
  const [open, setOpen] = useState(false);

  return (
    <Modal
      size="fullscreen"
      closeIcon
      open={open}
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      trigger={trigger}
    >
      <Modal.Header>{header}</Modal.Header>
      <Modal.Content scrolling>
        <Modal.Description>{children}</Modal.Description>
      </Modal.Content>
    </Modal>
  );
};

export default ModalScrollingContent;

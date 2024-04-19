import React, { useState } from 'react';
import { Upload, Button, Card, Space, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

function UploadPage() {
  const [fileList, setFileList] = useState([]);

  const onChange = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const onPreview = async file => {
    let src = file.url;
    if (!src) {
      src = await new Promise(resolve => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj);
        reader.onload = () => resolve(reader.result);
      });
    }
    const image = new Image();
    image.src = src;
    const imgWindow = window.open(src);
    imgWindow.document.write(image.outerHTML);
  };

  const uploadButton = (
    <div>
      <PlusOutlined />
      <div style={{ marginTop: 8 }}>Upload</div>
    </div>
  );

  return (
    <Space direction="vertical" size="large" style={{ display: 'flex', justifyContent: 'center', paddingTop: 50 }}>
      <Card title="Upload Your Photos" bordered={false} style={{ width: 300 }}>
        <Upload
          action="http://localhost:5000/api/upload"
          fileList={fileList}
          onChange={onChange}
          onPreview={onPreview}
          listType="picture-card"
        >
          {fileList.length >= 8 ? null : uploadButton}
        </Upload>
      </Card>
    </Space>
  );
}

export default UploadPage;

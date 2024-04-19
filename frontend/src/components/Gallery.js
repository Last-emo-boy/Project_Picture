import React from 'react';
import { motion } from 'framer-motion';


function Gallery({ images }) {
  return (
    <div className="gallery">
      {images.map(image => (
        <motion.div
          key={image.id}
          layout
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <img src={`http://localhost:5000/uploads/${image.filename}`} alt="uploaded" />
        </motion.div>
      ))}
    </div>
  );
}

export default Gallery;

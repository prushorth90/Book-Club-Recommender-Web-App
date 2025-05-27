import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

function Parragraph2(props) {
  return (
    <Typography component="body1" variant="body1" color="#23180a" gutterBottom>
      {props.children}
    </Typography>
  );
}

Parragraph2.propTypes = {
  children: PropTypes.node,
};

export default Parragraph2;
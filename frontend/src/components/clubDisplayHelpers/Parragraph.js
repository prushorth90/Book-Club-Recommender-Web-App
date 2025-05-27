import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

function Parragraph(props) {
  return (
    <Typography component="h2" variant="h6" color="#23180a" gutterBottom>
      {props.children}
    </Typography>
  );
}

Parragraph.propTypes = {
  children: PropTypes.node,
};

export default Parragraph;
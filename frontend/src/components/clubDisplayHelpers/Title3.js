import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

function Title3(props) {
  return (
    <Typography component="h2" variant="h2" color="#fff" gutterBottom>
      {props.children}
    </Typography>
  );
}

Title3.propTypes = {
  children: PropTypes.node,
};

export default Title3;
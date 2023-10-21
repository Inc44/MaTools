use pyo3::prelude::*;
use belilo::{process_directory, process_image};
use std::path::Path;

#[pymodule]
fn belilo_pyo3(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m, name = "process_image_py")]
    fn process_image_py(_py: Python, input_path: &str, override_flag: bool) -> PyResult<()> {
        let path = Path::new(input_path);
        process_image(&path, override_flag)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyException, _>(format!("{}", e)))
    }

    #[pyfn(m, name = "process_directory_py")]
    fn process_directory_py(_py: Python, input_path: &str, override_flag: bool) -> PyResult<()> {
        let path = Path::new(input_path);
        process_directory(&path, override_flag)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyException, _>(format!("{}", e)))
    }

    Ok(())
}

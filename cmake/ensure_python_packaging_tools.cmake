if(NOT DEFINED PYTHON_EXECUTABLE OR PYTHON_EXECUTABLE STREQUAL "")
    message(FATAL_ERROR "PYTHON_EXECUTABLE is required")
endif()

execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -m pip --version
    RESULT_VARIABLE _pip_result
    OUTPUT_QUIET
    ERROR_QUIET
)

if(NOT _pip_result EQUAL 0)
    message(FATAL_ERROR
        "Python interpreter '${PYTHON_EXECUTABLE}' does not have pip available. "
        "Install pip for this interpreter before building.")
endif()

execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -m pip install --disable-pip-version-check --upgrade build wheel setuptools
    RESULT_VARIABLE _bootstrap_result
    COMMAND_ECHO STDOUT
)

if(NOT _bootstrap_result EQUAL 0)
    message(FATAL_ERROR
        "Failed to install required Python packaging tools (build, wheel, setuptools) "
        "for interpreter '${PYTHON_EXECUTABLE}'.")
endif()
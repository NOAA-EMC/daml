#ecbuild_add_executable( TARGET daml_ice_emul.x
#                        SOURCES iceEmul.cc IceEmul.h BaseEmul.h)
#target_compile_features( daml_ice_emul.x  PUBLIC cxx_std_17)
#target_link_libraries( daml_ice_emul.x PUBLIC NetCDF::NetCDF_CXX oops atlas "${TORCH_LIBRARIES}")


#ecbuild_add_executable( TARGET daml_salt_emul.x
#                        SOURCES saltEmul.cc SaltEmul.h BaseEmul.h)
#target_compile_features( daml_salt_emul.x  PUBLIC cxx_std_17)
#target_link_libraries( daml_salt_emul.x PUBLIC NetCDF::NetCDF_CXX oops atlas "${TORCH_LIBRARIES}")

protoc \
  -I=. \
  --python_out=out \
  common/common.proto \
  examples1/test1.proto \
  examples2/test2.proto
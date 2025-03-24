BUILDDIR=./build/proto
PROTOPATH=./proto
mkdir -p $BUILDDIR
python -m grpc_tools.protoc \
    --proto_path=$PROTOPATH \
    --python_out=$BUILDDIR \
    --pyi_out=$BUILDDIR \
    --grpc_python_out=$BUILDDIR $PROTOPATH/pokemon_interface.proto

# 启用 ARM32 架构
sudo dpkg --add-architecture armhf
sudo apt update
# 安装交叉编译器和基础构建工具
sudo apt install -y gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf make build-essential
sudo apt install -y libpython3-dev:armhf libffi-dev:armhf libssl-dev:armhf zlib1g-dev:armhf

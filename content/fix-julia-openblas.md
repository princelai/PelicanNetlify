Title: 修复julia OpenBLAS不能正确加载的问题
Date: 2020-05-25 15:00
Category: 机器学习,金融与算法,玩电脑,杂记
Tags: julia
Slug: fix-julia-openblas
Authors: Kevin Chen
Status: draft

julia> using Libdl
julia> filter(p -> occursin("blas", p), Libdl.dllist())

julia> using OpenBLAS_jll
julia> filter(p -> occursin("blas", p), Libdl.dllist())

ldd ~/.julia/artifacts/8a63e55e4ce37cc04c039ac5f48c2a8b8e9b3b37/lib/libarpack.so
    libopenblas64_.so.0 => not found

    
yay -Ql openblas|grep ".so"
openblas /usr/lib/libblas.so
openblas /usr/lib/libblas.so.3
openblas /usr/lib/libopenblas.so
openblas /usr/lib/libopenblas.so.3
openblas /usr/lib/libopenblasp-r0.3.9.so


sudo ln -s /usr/lib/libopenblasp-r0.3.9.so /usr/lib/libopenblas64_.so.0

ll /usr/lib/ |grep libopenblas                                         
lrwxrwxrwx   1 root root    22  3月  4 19:05 libblas.so -> libopenblasp-r0.3.9.so
lrwxrwxrwx   1 root root    22  3月  4 19:05 libblas.so.3 -> libopenblasp-r0.3.9.so
lrwxrwxrwx   1 root root    31  5月 25 14:09 libopenblas64_.so.0 -> /usr/lib/libopenblasp-r0.3.9.so
-rwxr-xr-x   1 root root   18M  3月  4 19:05 libopenblasp-r0.3.9.so
lrwxrwxrwx   1 root root    22  3月  4 19:05 libopenblas.so -> libopenblasp-r0.3.9.so
lrwxrwxrwx   1 root root    22  3月  4 19:05 libopenblas.so.3 -> libopenblasp-r0.3.9.so


https://github.com/JuliaLinearAlgebra/Arpack.jl/issues/97
https://wiki.archlinux.org/index.php/Julia_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

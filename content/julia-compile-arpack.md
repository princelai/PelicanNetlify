Title: Julia编译Arpack失败的解决办法
Date: 2019-05-09 17:54
Category: 玩电脑
Tags: julia, arpack, gadfly
Slug: julia-compile-arpack
Authors: Kevin Chen




最近想学一门新语言，对于数据处理/算法/深度学习来说，除了Python外，Julia算是一门很有吸引力的语言，但是在安装绘图库Gadfly的时候遇到报错。

```julia
julia> using Gadfly
[ Info: Precompiling Gadfly [c91e804a-d5a3-530f-b6f0-dfbca275c004]
ERROR: LoadError: No deps.jl file could be found. Please try running Pkg.build("Arpack").
Currently, the build command might fail when Julia has been built from source
and the recommendation is to use the official binaries from julialang.org.
For more info see https://github.com/JuliaLinearAlgebra/Arpack.jl/issues/5.

Stacktrace:
 [1] top-level scope at /home/kevin/.julia/packages/Arpack/UiiMc/src/Arpack.jl:19
 [2] top-level scope at none:2
in expression starting at /home/kevin/.julia/packages/Arpack/UiiMc/src/Arpack.jl:16
ERROR: LoadError: LoadError: Failed to precompile Arpack [7d9fca2a-8960-54d3-9f78-7d1dccf2cb97] to /home/kevin/.julia/compiled/v1.1/Arpack/X5VZL.ji.
Stacktrace:
 [1] include at ./sysimg.jl:29 [inlined]
 [2] include(::String) at /home/kevin/.julia/packages/PDMats/AObTs/src/PDMats.jl:1
 [3] top-level scope at /home/kevin/.julia/packages/PDMats/AObTs/src/PDMats.jl:52
 [4] top-level scope at none:2
in expression starting at /home/kevin/.julia/packages/PDMats/AObTs/src/pdsparsemat.jl:1
in expression starting at /home/kevin/.julia/packages/PDMats/AObTs/src/PDMats.jl:51
ERROR: LoadError: Failed to precompile PDMats [90014a1f-27ba-587c-ab20-58faa44d9150] to /home/kevin/.julia/compiled/v1.1/PDMats/wuzEE.ji.
Stacktrace:
 [1] top-level scope at none:2
in expression starting at /home/kevin/.julia/packages/Distributions/wY4bz/src/Distributions.jl:3
ERROR: LoadError: Failed to precompile Distributions [31c24e10-a181-5473-b8eb-7969acd0382f] to /home/kevin/.julia/compiled/v1.1/Distributions/xILW0.ji.
Stacktrace:
 [1] top-level scope at none:2
in expression starting at /home/kevin/.julia/packages/Gadfly/09PWZ/src/Gadfly.jl:21
ERROR: Failed to precompile Gadfly [c91e804a-d5a3-530f-b6f0-dfbca275c004] to /home/kevin/.julia/compiled/v1.1/Gadfly/DvECm.ji.

```



根据提示，问题出在编译Arpack上，尝试手动编译。

```julia
julia> Pkg.build("Arpack")
  Building Arpack → `~/.julia/packages/Arpack/UiiMc/deps/build.log`
┌ Error: Error building `Arpack`: 
│ ERROR: LoadError: LibraryProduct(nothing, ["libarpack"], :libarpack, "Prefix(/home/kevin/.julia/packages/Arpack/UiiMc/deps/usr)") is not satisfied, cannot generate deps.jl!
│ Stacktrace:
│  [1] #write_deps_file#152(::Bool, ::Function, ::String, ::Array{LibraryProduct,1}) at /home/kevin/.julia/packages/BinaryProvider/TcAwt/src/Products.jl:414
│  [2] (::getfield(BinaryProvider, Symbol("#kw##write_deps_file")))(::NamedTuple{(:verbose,),Tuple{Bool}}, ::typeof(write_deps_file), ::String, ::Array{LibraryProduct,1}) at ./none:0
│  [3] top-level scope at none:0
│  [4] include(::String) at ./client.jl:403
│  [5] top-level scope at none:0
│ in expression starting at /home/kevin/.julia/packages/Arpack/UiiMc/deps/build.jl:74
└ @ Pkg.Operations /build/julia/src/julia-1.1.0/usr/share/julia/stdlib/v1.1/Pkg/src/Operations.jl:1075
```



同样遇到报错，Github Issues中没给出具体的解决办法，网上搜了一圈也没找到，决定自己尝试解决，尝试几次就找到了解决办法。





首先安装arpack包

`yaourt -S arpack`





安装完成后系统里就有动态链接库文件

```shell
ls -lh /usr/lib64/libarpack.so
lrwxrwxrwx 1 root root 18 Apr 23 07:28 /usr/lib64/libarpack.so -> libarpack.so.2.1.0
```





根据上面错误信息，知道Julia Arpack使用的so文件路径

```shell
ls -lh ～/.julia/packages/Arpack/UiiMc/deps/usr/lib

drwxr-xr-x 2 kevin kevin 4.0K Oct  4  2018 cmake
lrwxrwxrwx 1 kevin kevin   14 Oct  4  2018 libarpack.so -> libarpack.so.2
lrwxrwxrwx 1 kevin kevin   18 Oct  4  2018 libarpack.so.2 -> libarpack.so.2.0.0
-rwxr-xr-x 1 kevin kevin 367K Oct  4  2018 libarpack.so.2.0.0
```





使用系统arpack覆盖掉julia的so文件。

```shell
ln -s /usr/lib64/libarpack.so ~/.julia/packages/Arpack/UiiMc/deps/usr/lib/libarpack.so
```





最后，编译成功，可以正常使用Gadfly了。

```julia
julia> Pkg.build("Arpack")
  Building Arpack → `~/.julia/packages/Arpack/UiiMc/deps/build.log`
```

```julia
julia> using Gadfly
[ Info: Precompiling Gadfly [c91e804a-d5a3-530f-b6f0-dfbca275c004]
```


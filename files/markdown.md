“异步和性能”稍微偏重于在语言机制之上处理异步编程的模式。

异步不只是对应用的性能至关重要，而且正在慢慢成为代码易写性和可维护性方面的关键因素



---

### 前言

在之前的[浅谈 JavaScript Event Loop](https://juejin.cn/post/6844904078900723720)一文中简单介绍了事件循环的机制，了解了各种异步或者说在**将来**执行的任务的执行时间、执行顺序等。然而异步是如何出现的，为什么会使用异步，以及处理异步的方法，还有待探讨。

本文...

### 1. 异步之于 JavaScript

以浏览器宿主环境为例，页面的渲染、JS脚本的执行、事件的循环、定时器的触发以及HTTP请求，都在浏览器的内核即**渲染进程**内进行。其中，GUI渲染线程与JS引擎线程互斥，当JS引擎执行时GUI线程会被挂起，所以JS执行的时间过长就会造成页面的渲染不连贯，进而阻塞页面加载。

为了避免JS脚本执行时间过长，JavaScript引入了异步的任务执行模式。如网络请求、文件读取等需要等待耗时的操作可异步进行，而不阻塞 JS 执行线程。

#### 异步的运作模式

> JavaScript 程序总是至少分为两个块：第一块现在运行；下一块将来运行，以响应某个事件。

首先，“异步”并不代表“并行”：异步是关于现在和将来的时间间隙，而并行是关于能够同时发生的事情。

程序中“现在运行的部分”和“将来运行的部分”之间的关系是异步编程的核心。

TODO

### 2. 异步编程的方式

#### 2.1 回调

回调是编写和处理 JavaScript 程序异步逻辑的最常用的方式，是最基础的异步模式。

回调函数的优点是简单、容易理解和部署，缺点是不利于代码的阅读和维护，各个部分之间高度耦合，流程会很混乱，而且每个任务只能指定一个回调函数。

回调表达异步流程的方式是非线性的、非顺序的，这使得正确推导这样的代码难度很大。难于理解的代码是坏代码，会导致坏 bug。

受到控制反转的影响，控制的转移导致一系列麻烦的信任问题，比如回调被调用的次数是否会超出预期。

##### 回调地狱

##### 控制反转

也就是把自己程序一部分的执行控制交给某个第三方。信任问题：

> - 调用回调过早；
> - 调用回调过晚（或不被调用）；
> - 调用回调次数过少或过多；
> - 未能传递所需的环境和参数；
> - 吞掉可能出现的错误和异常。



#### 2.2 Promise

不把自己程序的continuation 传给第三方，而是希望第三方给我们提供了解其任务何时结束的能力，然后由我们自己的代码来决定下一步做什么。

一旦我需要的值准备好了，我就用我的承诺值（ value-promise）换取这个值本身。这个未来值可能成功，也可能失败。

Promise 的决议：一种在异步任务中作为两个或更多步骤的流程控制机制，时序上的 this-then-that。

反控制反转——把控制返还给调用代码。

把回调的安排转交给了一个位于我们和其他工具之间的可信任的中介机制。

promise 的决议函数：resolve(..) 通常标识完成，而 reject(..) 则标识拒绝。

Promise 链也以顺序的方式表达异步流，尽管并不完美。

#### 2.3 生成器

创建了一个迭代器对象，把它赋给了一个变量 it，用于控制生成器`*foo(..)`。然后调用 it.next()，指示生成器 *foo(..) 从当前位置开始继续运行，停在下一个 yield 处或者直到生成器结束。

next(..) 调用的结果是一个对象，它有一个 value 属性，持有从 *foo(..) 返回的值（如果有的话）。换句话说， yield 会导致生成器在执行过程中发送出一个值，这有点类似于 return。

第一个 next(..) 总是启动一个生成器，并运行到第一个 yield 处。

yield .. 和 next(..) 这一对组合起来， 在生成器的执行过程中，提供了暂停程序和恢复执行的机制，也构成了一个双向消息传递系统。一对一匹配，最后多出一个next(..) 接收return的值，若没有则为undefined

在异步控制流程方面，生成器的关键优点是：生成器内部的代码是以自然的同步 / 顺序方式表达任务的一系列步骤。

#### 2.4 async/await

组合 Promise 和看似同步的流程控制代码

### 3. 异步与性能



### 总结

### 参考资料

- 《你不知道的JavaScript（中卷）》
- [Javascript异步编程的4种方法](http://www.ruanyifeng.com/blog/2012/12/asynchronous%EF%BC%BFjavascript.html)

- [MDN | 使用 Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises)


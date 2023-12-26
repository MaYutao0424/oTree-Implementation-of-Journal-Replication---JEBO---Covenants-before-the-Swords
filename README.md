# oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords

## Project Purpose
- 我是一名实验经济学的爱好者，目前正在学习如何通过oTree工具完成实验设计
- 顶刊复刻是一种重要的学习方法，比如一些经济学实证研究者通过复刻顶刊代码进行Stata和计量的学习
- 对于实验经济学期刊论文也如此，通过顶刊复现，熟悉有关实验设计框架，练习oTree有关功能的实现
- 本次复刻的论文是 **《Covenants before the swords: The limits to efficient cooperation in heterogeneous groups》** (https://www.sciencedirect.com/science/article/pii/S016726812100189X) ，来自**Journal of Economic Behavior and Organization (JEBO) Volume 188, August 2021, Pages 307-321**
## Project Description
- 原文摘要如下：
> When agents derive heterogeneous benefits from cooperation, a tension between efficiency and equality often arises. This tension can impede agents’ ability to cooperate efficiently. We design a laboratory   experiment, in which we investigate the capacity of communication and punishment, separately and jointly, to promote cooperation in such an environment. Our results reveal that cooperation and earnings are significantly greater when both communication and punishment (a sword) are possible than when only one is available. Both cooperation levels and earnings, however, still fall substantially below the maximum possible. The reason is that groups establish covenants, i.e. mutual contribution agreements, that tend to strike a compromise between efficiency and equality. The timing of communication is critical. A history of sanctioning substantially reduces the probability that groups subsequently establish a covenant. Overall, our findings indicate not only the benefits of early communication, but also some limits to efficient cooperation in heterogeneous groups
- 简单来说，这是一个在**公共品博弈范式**的基础上，添加了**沟通和惩罚**处理条件的实验。作者想要探究在存在异质性的群体中，交流和惩罚（单独或联合使用）对促进合作的效果。详细内容可以参考原文
- 在oTree复刻中，仍保留了原文实现的核心功能，包括**角色划分、沟通、贡献分配、惩罚与反击**，但为简便起见，在轮次、页面跳转等方面做了调整
- b站视频演示：https://www.bilibili.com/video/BV1bT4y1s77c/?vd_source=77a3d9721321c3e4c44bacd0350cda67
## Examples
### Contribute
- 实验中，4人为一个小组，他们要完成一个公共品博弈实验。玩家被分为公共池收益系数为0.3的Type A或0.6的Type B，每组两位Type A和两位Type B
![contribution](https://github.com/745985789/oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords/assets/90327043/3f801348-27be-4ca2-8cb0-5fc659ce22b7)
### Chatroom
- 在一定轮次，同一组的玩家可以通过聊天室交流。聊天室中有两种频道，公共频道和专属频道。同组中的4人都可以在公共频道中发送和接收信息，而在专属频道，只有同类型的2人才可以交流
![chatroom](https://github.com/745985789/oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords/assets/90327043/2b8dc920-f3dd-4ab4-9b29-a372db8ae2b2)
### AllocationStage1
- 在一定轮次，当公布完所有人的捐赠结果后，你可以向他人分配点数用于惩罚。你向他人分配的每一点数都会致使该玩家的最终收益减少一点数。如果你执行了分配点数的操作，你需要从总收益中扣除一点的分配费
![allocation1](https://github.com/745985789/oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords/assets/90327043/d491be53-d302-42fa-b0de-129e98a15d8a)
### AllocationStage2
- 在上述惩罚阶段后，会展示惩罚结果，包括你向哪些人分配了点数，哪些人像你分配了点数。由于该环节使用了实时页面方法，你可以向他人再次追加分配点数来反击，他人也可以向你发动攻击，页面结果每15s自动刷新一次(你也可以手动刷新结果)。直到所有人不再向他人分配点数时，该轮次结束
![allocation2](https://github.com/745985789/oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords/assets/90327043/fcf4f153-876e-4718-93ee-0a6fea1a853d)
### Finalresults
![finalresults](https://github.com/745985789/oTree-Implementation-of-Journal-Replication---JEBO---Covenants-before-the-Swords/assets/90327043/68cfa8d0-97f7-4760-a4eb-01d78f21cafc)



class TinyEmitter:
    def __init__(self):
        # 初始化事件存储字典，键为事件名，值为回调函数列表
        self.events = {}

    def on(self, event, func, context=None):
        """注册事件监听器"""
        # 如果事件不存在，初始化一个空列表
        if event not in self.events:
            self.events[event] = []
        # 存储回调函数和上下文
        self.events[event].append({"fn": func, "ctx": context})
        return self

    def once(self, event, func, context=None):
        """注册一次性事件监听器，触发后自动移除"""
        emitter = self

        # 包装原始函数，使其触发后自动解绑
        def wrapper(*args, **kwargs):
            # 先解绑事件
            emitter.off(event, wrapper)
            # 再执行原始函数
            return func(*args, **kwargs)

        # 保存原始函数引用，用于off方法识别
        wrapper._original = func
        return self.on(event, wrapper, context)

    def emit(self, event, *args, **kwargs):
        """触发指定事件的所有监听器"""
        # 如果事件不存在，直接返回
        if event not in self.events:
            return self

        # 复制一份回调列表，防止在触发过程中修改列表导致问题
        callbacks = self.events[event][:]
        for callback in callbacks:
            func = callback["fn"]
            ctx = callback["ctx"]
            # 如果有上下文，使用上下文调用函数，否则直接调用
            if ctx:
                func.apply(ctx, args, kwargs)
            else:
                func(*args, **kwargs)
        return self

    def off(self, event, func):
        """移除事件监听器"""
        if event not in self.events:
            return self

        # 过滤掉要移除的函数
        new_callbacks = []
        for callback in self.events[event]:
            # 检查是否是原始函数或once包装的函数
            if callback["fn"] != func and getattr(callback["fn"], "_original", None) != func:
                new_callbacks.append(callback)

        # 更新事件的回调列表，如果为空则删除该事件
        if new_callbacks:
            self.events[event] = new_callbacks
        else:
            del self.events[event]
        return self

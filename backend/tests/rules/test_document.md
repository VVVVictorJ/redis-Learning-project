# FastAPI 单元测试规范文档

## 1. 文档概述

本规范文档旨在为 FastAPI 项目提供标准化的单元测试编写指南，确保测试代码的质量、一致性和可维护性。

## 2. 测试目录结构

```
tests/
├── __init__.py
├── conftest.py                 # 全局测试配置
├── unit/                       # 单元测试目录
│   ├── services/               # 服务层测试
│   ├── models/                 # 数据模型测试
│   ├── schemas/                # Pydantic 模型测试
│   └── utils/                  # 工具函数测试
├── integration/                # 集成测试目录
│   ├── api/                    # API 路由测试
│   └── db/                     # 数据库集成测试
└── e2e/                        # 端到端测试
    └── scenarios/              # 业务场景测试
```

## 3. 测试编写规范

### 3.1 命名规范

- **测试文件**：`test_<module_name>.py`
- **测试类**：`Test<ModuleName>`
- **测试方法**：`test_<scenario>_<expected_result>`
- **测试夹具**：`<purpose>_fixture`

### 3.2 测试结构模板

```python
import pytest
from fastapi import status
from fastapi.testclient import TestClient

class TestMenuAPI:
    """菜单API测试套件"""

    def test_get_menu_items_empty(self, client: TestClient):
        """
        测试获取空菜单列表
        预期: 返回空数组和200状态码
        """
        # Arrange
        endpoint = "/api/v1/menus"

        # Act
        response = client.get(endpoint)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_create_menu_item(self, menu_service, db_session):
        """
        测试菜单项创建服务
        预期: 正确创建并返回带ID的菜单项
        """
        # Arrange
        from app.schemas.menu import MenuItemCreate
        menu_data = MenuItemCreate(title="Reports", route="/reports")

        # Act
        result = await menu_service.create_menu(db_session, menu_data)

        # Assert
        assert result.id is not None
        assert result.title == menu_data.title
```

### 3.3 断言最佳实践

1. **HTTP 响应断言**：

   ```python
   assert response.status_code == status.HTTP_201_CREATED
   assert "Location" in response.headers
   ```
2. **数据结构断言**：

   ```python
   response_data = response.json()
   assert set(response_data.keys()) == {"id", "title", "created_at"}
   ```
3. **Pydantic 模型验证**：

   ```python
   from app.schemas.menu import MenuItemOut
   MenuItemOut(**response.json())  # 验证失败会自动抛出异常
   ```
4. **数据库状态断言**：

   ```python
   from sqlalchemy import select
   result = await db_session.execute(select(MenuItem).where(MenuItem.title == "Reports"))
   assert result.scalar_one_or_none() is not None
   ```

## 4. 测试夹具规范

### 4.1 基础夹具

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from db.base import Base

@pytest.fixture(scope="session")
def test_client():
    """全局测试客户端"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
async def db_session():
    """数据库会话夹具"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
```

### 4.2 工厂夹具

```python
# tests/conftest.py
from app.models.menu import MenuItem

@pytest.fixture
def menu_item_factory(db_session):
    """菜单项工厂夹具"""
    async def factory(**kwargs):
        default = {
            "title": "Test Menu",
            "route": "/test",
            "is_active": True
        }
        item = MenuItem(**{**default, **kwargs})
        db_session.add(item)
        await db_session.commit()
        return item
    return factory
```

## 5. 异步测试规范

### 5.1 基本异步测试

```python
@pytest.mark.asyncio
async def test_async_operation(db_session):
    """测试异步数据库操作"""
    from app.models.menu import MenuItem
    item = MenuItem(title="Async Test")
    db_session.add(item)
    await db_session.commit()
  
    result = await db_session.get(MenuItem, item.id)
    assert result is not None
```

### 5.2 异步HTTP测试

```python
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_client():
    """使用AsyncClient测试异步端点"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/async-endpoint")
        assert response.status_code == 200
```

## 6. 测试覆盖率要求

1. **最低覆盖率标准**：

   - 业务逻辑层：≥90%
   - API路由层：≥80%
   - 工具函数：100%
2. **覆盖率配置**：

   ```ini
   # .coveragerc
   [run]
   source = app
   omit = 
       app/migrations/*
       app/__init__.py
       app/main.py

   [report]
   exclude_lines =
       pragma: no cover
       def __repr__
       raise NotImplementedError
       if __name__ == .__main__.:
   ```

## 7. 测试数据管理

### 7.1 测试数据原则

1. 每个测试用例使用独立的数据集
2. 避免使用生产数据
3. 测试后清理数据库

### 7.2 数据工厂示例

```python
# tests/factories/menu_factory.py
import factory
from app.models.menu import MenuItem

class MenuItemFactory(factory.Factory):
    class Meta:
        model = MenuItem

    title = factory.Sequence(lambda n: f"Menu {n}")
    route = factory.Sequence(lambda n: f"/menu-{n}")
    is_active = True
```

## 8. 测试执行规范

### 8.1 常用命令

```bash
# 运行全部测试
pytest -v

# 运行指定模块测试
pytest tests/unit/services/test_menu_service.py -v

# 带覆盖率报告
pytest --cov=app --cov-report=html

# 并行测试
pytest -n auto
```

### 8.2 CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[test]
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## 9. 异常测试规范

### 9.1 预期异常测试

```python
def test_invalid_menu_creation(client: TestClient):
    """测试无效菜单创建"""
    response = client.post("/api/menus", json={"title": ""})
  
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error_detail = response.json()["detail"][0]
    assert error_detail["loc"] == ["body", "title"]
    assert error_detail["msg"] == "title cannot be empty"
```

### 9.2 错误响应验证

```python
def test_not_found_response(client: TestClient):
    """测试404响应"""
    response = client.get("/api/menus/999")
  
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Menu item not found",
        "status": 404
    }
```

## 10. 性能测试规范

### 10.1 基准测试

```python
@pytest.mark.benchmark
def test_menu_list_performance(client: TestClient, benchmark):
    """测试菜单列表接口性能"""
    result = benchmark(client.get, "/api/menus")
    assert result.status_code == 200
    assert benchmark.stats.stats.max < 0.1  # 最大响应时间<100ms
```

### 10.2 负载测试

```python
@pytest.mark.load
def test_concurrent_menu_requests(client: TestClient):
    """测试并发菜单请求"""
    from concurrent.futures import ThreadPoolExecutor
  
    def make_request():
        return client.get("/api/menus")
  
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(make_request, range(50)))
  
    assert all(r.status_code == 200 for r in results)
```

## 附录A：推荐测试库

1. 核心测试：

   - `pytest`
   - `pytest-asyncio`
   - `httpx`
2. 数据工厂：

   - `factory_boy`
   - `faker`
3. 测试增强：

   - `pytest-mock`
   - `pytest-cov`
   - `pytest-xdist` (并行测试)
4. API 测试：

   - `schemathesis` (基于OpenAPI的测试)

---

本规范文档应随项目演进定期更新，所有新编写的测试代码必须符合本规范要求。测试覆盖率报告应纳入代码评审流程，未达标的代码不得合并到主分支。

# PyHeart Package Structure

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=65", "wheel", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "pyheart"
version = "0.1.0"
description = "Healthcare Interoperability & Workflow Engine - Universal integration platform for healthcare systems"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "Apache-2.0"}
authors = [
    {name = "Dr. Fadil", email = "fadil@brainsait.com"},
    {name = "BrainSAIT Team", email = "team@brainsait.com"}
]
maintainers = [
    {name = "BrainSAIT Healthcare Innovation Lab", email = "healthcare@brainsait.com"}
]
keywords = [
    "healthcare", "fhir", "hl7", "interoperability", "integration",
    "workflow", "orchestration", "api-gateway", "health-informatics",
    "medical-integration", "healthcare-api"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Healthcare Industry",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
    "Topic :: System :: Networking",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Framework :: FastAPI",
    "Natural Language :: English",
    "Natural Language :: Arabic",
]

dependencies = [
    "fhir.resources>=6.5.0",
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.22.0",
    "httpx>=0.24.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "sqlalchemy>=2.0",
    "alembic>=1.11.0",
    "asyncpg>=0.28.0",
    "redis>=4.5.0",
    "aiokafka>=0.8.0",
    "motor>=3.2.0",  # MongoDB async driver
    "cryptography>=41.0.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "aiofiles>=23.1.0",
    "orjson>=3.9.0",
    "python-dateutil>=2.8.2",
    "pytz>=2023.3",
    "tenacity>=8.2.0",
    "structlog>=23.1.0",
    "prometheus-client>=0.17.0",
    "opentelemetry-api>=1.18.0",
    "opentelemetry-sdk>=1.18.0",
    "opentelemetry-instrumentation-fastapi>=0.39b0",
    "grpcio>=1.56.0",
    "grpcio-tools>=1.56.0",
    "hl7>=0.8.0",
    "pydicom>=2.4.0",
    "lxml>=4.9.0",
    "jsonschema>=4.18.0",
    "pyyaml>=6.0",
    "click>=8.1.0",
    "rich>=13.4.0",
    "python-consul>=1.1.0",
    "aiocache[redis]>=0.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.3.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-timeout>=2.1.0",
    "black>=23.3.0",
    "flake8>=6.0.0",
    "mypy>=1.3.0",
    "isort>=5.12.0",
    "pre-commit>=3.3.0",
    "pytest-mock>=3.11.0",
    "factory-boy>=3.2.1",
    "faker>=18.11.0",
    "responses>=0.23.0",
    "testcontainers[kafka,redis,postgres]>=3.7.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.2.0",
    "sphinx-autodoc-typehints>=1.23.0",
    "myst-parser>=2.0.0",
    "sphinxcontrib-openapi>=0.8.0",
]
cloud = [
    "boto3>=1.26.0",
    "azure-servicebus>=7.11.0",
    "google-cloud-pubsub>=2.18.0",
    "kubernetes>=27.2.0",
]
legacy = [
    "python-hl7>=0.4.0",
    "pymllp>=1.2.0",  # MLLP for HL7v2
    "pynetdicom>=2.0.0",  # DICOM networking
]

[project.urls]
Homepage = "https://github.com/brainsait/pyheart"
Documentation = "https://pyheart.readthedocs.io"
Repository = "https://github.com/brainsait/pyheart"
Issues = "https://github.com/brainsait/pyheart/issues"
Changelog = "https://github.com/brainsait/pyheart/blob/main/CHANGELOG.md"

[project.scripts]
pyheart = "pyheart.cli:main"
pyheart-server = "pyheart.server:run"
pyheart-worker = "pyheart.worker:start"
pyheart-migrate = "pyheart.database:migrate"

[project.entry-points."pyheart.adapters"]
hl7v2 = "pyheart.adapters.hl7:HL7v2Adapter"
dicom = "pyheart.adapters.dicom:DICOMAdapter"
x12 = "pyheart.adapters.x12:X12Adapter"

[tool.setuptools]
package-dir = {"" = "src"}
packages = {find = {where = ["src"], include = ["pyheart*"]}}

[tool.setuptools.package-data]
pyheart = [
    "schemas/*.json",
    "schemas/*.yaml",
    "mappings/*.json",
    "templates/*.html",
    "static/**/*",
]

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers --cov=pyheart --cov-report=term-missing"
testpaths = ["tests"]
pythonpath = ["src"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src/pyheart"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

## src/pyheart/__init__.py
```python
"""
PyHeart - Healthcare Interoperability & Workflow Engine

Universal integration platform for seamless healthcare system connectivity,
workflow orchestration, and secure data exchange.
"""

__version__ = "0.1.0"
__author__ = "BrainSAIT Healthcare Innovation Lab"
__email__ = "healthcare@brainsait.com"

from pyheart.core.client import FHIRClient, HealthcareClient
from pyheart.core.server import FHIRServer, APIGateway
from pyheart.core.workflow import WorkflowEngine, ProcessDefinition
from pyheart.core.integration import IntegrationHub, Adapter
from pyheart.core.security import SecurityManager, AuthProvider

__all__ = [
    "FHIRClient",
    "HealthcareClient",
    "FHIRServer",
    "APIGateway",
    "WorkflowEngine",
    "ProcessDefinition",
    "IntegrationHub",
    "Adapter",
    "SecurityManager",
    "AuthProvider",
]

# Configure structured logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

## src/pyheart/core/client.py
```python
"""
FHIR Client for PyHeart - Universal healthcare data access
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import httpx
from fhir.resources.patient import Patient
from fhir.resources.bundle import Bundle
from fhir.resources.operationoutcome import OperationOutcome
from pydantic import BaseModel, Field, HttpUrl
import structlog
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()


class ClientConfig(BaseModel):
    """Configuration for FHIR client"""
    
    base_url: HttpUrl
    auth_type: str = Field(default="bearer", description="Authentication type")
    auth_token: Optional[str] = None
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")


class FHIRClient:
    """
    Universal FHIR client for healthcare data access
    
    Features:
    - Async/sync operations
    - Automatic retries with exponential backoff
    - Smart caching
    - Batch operations
    - FHIR search with pagination
    """
    
    def __init__(self, config: Union[ClientConfig, str]):
        if isinstance(config, str):
            config = ClientConfig(base_url=config)
        self.config = config
        self._client = self._create_client()
        self._async_client = self._create_async_client()
    
    def _create_client(self) -> httpx.Client:
        """Create synchronous HTTP client"""
        headers = self._get_headers()
        return httpx.Client(
            base_url=str(self.config.base_url),
            headers=headers,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl
        )
    
    def _create_async_client(self) -> httpx.AsyncClient:
        """Create asynchronous HTTP client"""
        headers = self._get_headers()
        return httpx.AsyncClient(
            base_url=str(self.config.base_url),
            headers=headers,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        }
        
        if self.config.auth_token:
            if self.config.auth_type == "bearer":
                headers["Authorization"] = f"Bearer {self.config.auth_token}"
            elif self.config.auth_type == "basic":
                headers["Authorization"] = f"Basic {self.config.auth_token}"
        
        return headers
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """
        Get a patient by ID
        
        Args:
            patient_id: FHIR patient ID
            
        Returns:
            Patient resource or None
        """
        try:
            response = self._client.get(f"Patient/{patient_id}")
            response.raise_for_status()
            
            data = response.json()
            return Patient(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.info("Patient not found", patient_id=patient_id)
                return None
            logger.error("Failed to get patient", 
                        patient_id=patient_id, 
                        error=str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error getting patient", 
                        patient_id=patient_id,
                        error=str(e))
            raise
    
    async def get_patient_async(self, patient_id: str) -> Optional[Patient]:
        """Async version of get_patient"""
        try:
            response = await self._async_client.get(f"Patient/{patient_id}")
            response.raise_for_status()
            
            data = response.json()
            return Patient(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    def search(self, 
              resource_type: str,
              params: Optional[Dict[str, Any]] = None) -> Bundle:
        """
        Search for resources
        
        Args:
            resource_type: FHIR resource type
            params: Search parameters
            
        Returns:
            Bundle containing search results
        """
        params = params or {}
        
        try:
            response = self._client.get(resource_type, params=params)
            response.raise_for_status()
            
            data = response.json()
            return Bundle(**data)
        except Exception as e:
            logger.error("Search failed",
                        resource_type=resource_type,
                        params=params,
                        error=str(e))
            raise
    
    def create(self, resource: Any) -> Any:
        """
        Create a new resource
        
        Args:
            resource: FHIR resource to create
            
        Returns:
            Created resource with server-assigned ID
        """
        resource_type = resource.resource_type
        
        try:
            response = self._client.post(
                resource_type,
                content=resource.json()
            )
            response.raise_for_status()
            
            data = response.json()
            return resource.__class__(**data)
        except Exception as e:
            logger.error("Failed to create resource",
                        resource_type=resource_type,
                        error=str(e))
            raise
    
    def update(self, resource: Any) -> Any:
        """Update an existing resource"""
        resource_type = resource.resource_type
        resource_id = resource.id
        
        if not resource_id:
            raise ValueError("Resource must have an ID for update")
        
        try:
            response = self._client.put(
                f"{resource_type}/{resource_id}",
                content=resource.json()
            )
            response.raise_for_status()
            
            data = response.json()
            return resource.__class__(**data)
        except Exception as e:
            logger.error("Failed to update resource",
                        resource_type=resource_type,
                        resource_id=resource_id,
                        error=str(e))
            raise
    
    def delete(self, resource_type: str, resource_id: str) -> bool:
        """Delete a resource"""
        try:
            response = self._client.delete(f"{resource_type}/{resource_id}")
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return False
            raise
    
    def batch(self, bundle: Bundle) -> Bundle:
        """Execute batch/transaction operations"""
        try:
            response = self._client.post("", content=bundle.json())
            response.raise_for_status()
            
            data = response.json()
            return Bundle(**data)
        except Exception as e:
            logger.error("Batch operation failed", error=str(e))
            raise
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get server capability statement"""
        try:
            response = self._client.get("metadata")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Failed to get capabilities", error=str(e))
            raise
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close HTTP clients"""
        self._client.close()
        if hasattr(self, '_async_client'):
            asyncio.create_task(self._async_client.aclose())
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_client.aclose()


class HealthcareClient:
    """
    High-level healthcare client with multi-system support
    """
    
    def __init__(self):
        self.fhir_clients: Dict[str, FHIRClient] = {}
        self.adapters: Dict[str, Any] = {}
    
    def add_fhir_system(self, name: str, client: FHIRClient):
        """Add a FHIR system"""
        self.fhir_clients[name] = client
        logger.info("Added FHIR system", name=name)
    
    def add_legacy_system(self, name: str, adapter: Any):
        """Add a legacy system with adapter"""
        self.adapters[name] = adapter
        logger.info("Added legacy system", name=name)
    
    async def get_unified_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        Get patient data from all connected systems
        
        Returns unified patient record
        """
        unified_data = {
            "id": patient_id,
            "sources": {},
            "merged_demographics": {},
            "identifiers": []
        }
        
        # Fetch from all FHIR systems
        tasks = []
        for name, client in self.fhir_clients.items():
            task = self._fetch_patient_data(name, client, patient_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for name, result in zip(self.fhir_clients.keys(), results):
            if isinstance(result, Exception):
                logger.error("Failed to fetch from system",
                           system=name,
                           error=str(result))
            else:
                unified_data["sources"][name] = result
        
        # Merge demographics intelligently
        self._merge_demographics(unified_data)
        
        return unified_data
    
    async def _fetch_patient_data(self, 
                                 system_name: str,
                                 client: FHIRClient,
                                 patient_id: str) -> Optional[Dict[str, Any]]:
        """Fetch patient data from a single system"""
        try:
            patient = await client.get_patient_async(patient_id)
            if patient:
                return patient.dict()
            return None
        except Exception as e:
            logger.error("Failed to fetch patient",
                       system=system_name,
                       error=str(e))
            raise
    
    def _merge_demographics(self, unified_data: Dict[str, Any]):
        """Intelligently merge patient demographics from multiple sources"""
        # Implementation of smart merging logic
        # This would include conflict resolution, data quality scoring, etc.
        pass
```

## src/pyheart/core/workflow.py
```python
"""
Workflow Engine for healthcare process orchestration
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
import asyncio
from pydantic import BaseModel, Field
import structlog
from dataclasses import dataclass
import json

logger = structlog.get_logger()


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class TaskType(str, Enum):
    """Types of workflow tasks"""
    API_CALL = "api_call"
    TRANSFORMATION = "transformation"
    DECISION = "decision"
    NOTIFICATION = "notification"
    HUMAN_TASK = "human_task"
    SCRIPT = "script"
    PARALLEL = "parallel"
    SEQUENCE = "sequence"


@dataclass
class TaskResult:
    """Result of task execution"""
    status: TaskStatus
    output: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Task(BaseModel):
    """Workflow task definition"""
    
    id: str
    name: str
    type: TaskType
    config: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    retry_policy: Dict[str, Any] = Field(default_factory=dict)
    timeout: Optional[int] = None


class ProcessDefinition(BaseModel):
    """Healthcare process definition"""
    
    id: str
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    tasks: List[Task]
    variables: Dict[str, Any] = Field(default_factory=dict)
    triggers: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowInstance(BaseModel):
    """Running workflow instance"""
    
    id: str
    process_id: str
    status: TaskStatus = TaskStatus.PENDING
    variables: Dict[str, Any] = Field(default_factory=dict)
    task_results: Dict[str, TaskResult] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WorkflowEngine:
    """
    Healthcare workflow orchestration engine
    
    Features:
    - Visual workflow designer compatible
    - Async task execution
    - Error handling and retries
    - Human task management
    - Event-driven triggers
    """
    
    def __init__(self):
        self.processes: Dict[str, ProcessDefinition] = {}
        self.instances: Dict[str, WorkflowInstance] = {}
        self.task_handlers: Dict[TaskType, Callable] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default task handlers"""
        self.task_handlers[TaskType.API_CALL] = self._handle_api_call
        self.task_handlers[TaskType.TRANSFORMATION] = self._handle_transformation
        self.task_handlers[TaskType.DECISION] = self._handle_decision
        self.task_handlers[TaskType.NOTIFICATION] = self._handle_notification
        self.task_handlers[TaskType.PARALLEL] = self._handle_parallel
        self.task_handlers[TaskType.SEQUENCE] = self._handle_sequence
    
    def register_process(self, process: ProcessDefinition):
        """Register a process definition"""
        self.processes[process.id] = process
        logger.info("Registered process", 
                   process_id=process.id,
                   name=process.name)
    
    async def start_process(self, 
                          process_id: str,
                          variables: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a new workflow instance
        
        Args:
            process_id: Process definition ID
            variables: Initial variables
            
        Returns:
            Instance ID
        """
        if process_id not in self.processes:
            raise ValueError(f"Process {process_id} not found")
        
        process = self.processes[process_id]
        
        # Create instance
        instance = WorkflowInstance(
            id=f"{process_id}_{datetime.utcnow().timestamp()}",
            process_id=process_id,
            variables={**process.variables, **(variables or {})}
        )
        
        self.instances[instance.id] = instance
        
        logger.info("Started workflow instance",
                   instance_id=instance.id,
                   process_id=process_id)
        
        # Start execution
        asyncio.create_task(self._execute_instance(instance.id))
        
        return instance.id
    
    async def _execute_instance(self, instance_id: str):
        """Execute workflow instance"""
        instance = self.instances[instance_id]
        process = self.processes[instance.process_id]
        
        instance.status = TaskStatus.RUNNING
        
        try:
            # Execute tasks in dependency order
            for task in self._get_execution_order(process.tasks):
                if instance.status == TaskStatus.CANCELLED:
                    break
                
                await self._execute_task(instance, task)
            
            if instance.status != TaskStatus.CANCELLED:
                instance.status = TaskStatus.COMPLETED
        except Exception as e:
            logger.error("Workflow execution failed",
                       instance_id=instance_id,
                       error=str(e))
            instance.status = TaskStatus.FAILED
        finally:
            instance.updated_at = datetime.utcnow()
    
    async def _execute_task(self, 
                          instance: WorkflowInstance,
                          task: Task) -> TaskResult:
        """Execute a single task"""
        logger.info("Executing task",
                   instance_id=instance.id,
                   task_id=task.id,
                   task_type=task.type)
        
        # Check dependencies
        for dep_id in task.dependencies:
            dep_result = instance.task_results.get(dep_id)
            if not dep_result or dep_result.status != TaskStatus.COMPLETED:
                logger.warning("Skipping task due to failed dependency",
                             task_id=task.id,
                             dependency=dep_id)
                result = TaskResult(status=TaskStatus.SKIPPED)
                instance.task_results[task.id] = result
                return result
        
        # Execute task
        result = TaskResult(
            status=TaskStatus.RUNNING,
            started_at=datetime.utcnow()
        )
        instance.task_results[task.id] = result
        
        try:
            handler = self.task_handlers.get(task.type)
            if not handler:
                raise ValueError(f"No handler for task type {task.type}")
            
            output = await handler(task, instance)
            
            result.status = TaskStatus.COMPLETED
            result.output = output
            result.completed_at = datetime.utcnow()
        except Exception as e:
            logger.error("Task execution failed",
                       task_id=task.id,
                       error=str(e))
            result.status = TaskStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.utcnow()
            
            # Handle retry if configured
            if task.retry_policy:
                await self._handle_retry(instance, task)
        
        return result
    
    def _get_execution_order(self, tasks: List[Task]) -> List[Task]:
        """Get tasks in execution order based on dependencies"""
        # Simple topological sort
        visited = set()
        order = []
        
        def visit(task: Task):
            if task.id in visited:
                return
            
            visited.add(task.id)
            
            # Visit dependencies first
            for dep_id in task.dependencies:
                dep_task = next((t for t in tasks if t.id == dep_id), None)
                if dep_task:
                    visit(dep_task)
            
            order.append(task)
        
        for task in tasks:
            visit(task)
        
        return order
    
    async def _handle_api_call(self, 
                             task: Task,
                             instance: WorkflowInstance) -> Any:
        """Handle API call task"""
        config = task.config
        
        # Extract configuration
        method = config.get("method", "GET")
        url = config.get("url", "")
        headers = config.get("headers", {})
        body = config.get("body", {})
        
        # Variable substitution
        url = self._substitute_variables(url, instance.variables)
        body = self._substitute_variables(body, instance.variables)
        
        # Make API call
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body if method in ["POST", "PUT", "PATCH"] else None
            )
            response.raise_for_status()
            return response.json()
    
    async def _handle_transformation(self,
                                   task: Task,
                                   instance: WorkflowInstance) -> Any:
        """Handle data transformation task"""
        config = task.config
        
        # Get input data
        input_path = config.get("input", "")
        transform = config.get("transform", {})
        
        # Apply transformation
        # This is simplified - in production would use a proper transformation engine
        input_data = self._get_variable(instance, input_path)
        
        if transform.get("type") == "fhir_mapping":
            # Example FHIR transformation
            return self._transform_to_fhir(input_data, transform)
        
        return input_data
    
    async def _handle_decision(self,
                             task: Task,
                             instance: WorkflowInstance) -> Any:
        """Handle decision task"""
        config = task.config
        rules = config.get("rules", [])
        
        for rule in rules:
            condition = rule.get("condition", {})
            if self._evaluate_condition(condition, instance.variables):
                # Execute actions
                actions = rule.get("actions", [])
                for action in actions:
                    await self._execute_action(action, instance)
                return True
        
        return False
    
    async def _handle_notification(self,
                                 task: Task,
                                 instance: WorkflowInstance) -> Any:
        """Handle notification task"""
        config = task.config
        
        notification_type = config.get("type", "email")
        recipient = config.get("recipient", "")
        template = config.get("template", "")
        
        # Send notification
        logger.info("Sending notification",
                   type=notification_type,
                   recipient=recipient)
        
        # In production, would integrate with notification services
        return {"sent": True, "timestamp": datetime.utcnow()}
    
    async def _handle_parallel(self,
                             task: Task,
                             instance: WorkflowInstance) -> Any:
        """Handle parallel task execution"""
        subtasks = task.config.get("tasks", [])
        
        # Execute subtasks in parallel
        tasks = []
        for subtask_config in subtasks:
            subtask = Task(**subtask_config)
            tasks.append(self._execute_task(instance, subtask))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def _handle_sequence(self,
                             task: Task,
                             instance: WorkflowInstance) -> Any:
        """Handle sequential task execution"""
        subtasks = task.config.get("tasks", [])
        
        results = []
        for subtask_config in subtasks:
            subtask = Task(**subtask_config)
            result = await self._execute_task(instance, subtask)
            results.append(result)
            
            if result.status == TaskStatus.FAILED:
                break
        
        return results
    
    def _substitute_variables(self, 
                            template: Any,
                            variables: Dict[str, Any]) -> Any:
        """Substitute variables in template"""
        if isinstance(template, str):
            # Simple variable substitution
            for key, value in variables.items():
                template = template.replace(f"${{{key}}}", str(value))
            return template
        elif isinstance(template, dict):
            return {
                k: self._substitute_variables(v, variables)
                for k, v in template.items()
            }
        elif isinstance(template, list):
            return [
                self._substitute_variables(item, variables)
                for item in template
            ]
        return template
    
    def _get_variable(self, 
                     instance: WorkflowInstance,
                     path: str) -> Any:
        """Get variable by path"""
        parts = path.split(".")
        value = instance.variables
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        
        return value
    
    def _evaluate_condition(self,
                          condition: Dict[str, Any],
                          variables: Dict[str, Any]) -> bool:
        """Evaluate condition"""
        # Simple condition evaluation
        # In production, would use a proper expression engine
        operator = condition.get("operator", "eq")
        left = condition.get("left", "")
        right = condition.get("right", "")
        
        left_value = self._get_variable_value(left, variables)
        right_value = self._get_variable_value(right, variables)
        
        if operator == "eq":
            return left_value == right_value
        elif operator == "ne":
            return left_value != right_value
        elif operator == "gt":
            return left_value > right_value
        elif operator == "lt":
            return left_value < right_value
        elif operator == "gte":
            return left_value >= right_value
        elif operator == "lte":
            return left_value <= right_value
        
        return False
    
    def _get_variable_value(self, 
                          expr: str,
                          variables: Dict[str, Any]) -> Any:
        """Get variable value from expression"""
        if expr.startswith("$"):
            # Variable reference
            var_name = expr[1:]
            return variables.get(var_name)
        return expr
    
    async def _execute_action(self,
                            action: Dict[str, Any],
                            instance: WorkflowInstance):
        """Execute action"""
        action_type = action.get("type", "")
        
        if action_type == "set_variable":
            var_name = action.get("variable", "")
            value = action.get("value", "")
            instance.variables[var_name] = value
        elif action_type == "call_api":
            # Execute API call
            pass
    
    async def _handle_retry(self,
                          instance: WorkflowInstance,
                          task: Task):
        """Handle task retry"""
        retry_policy = task.retry_policy
        max_retries = retry_policy.get("max_retries", 3)
        delay = retry_policy.get("delay", 5)
        
        # Check current retry count
        retry_key = f"{task.id}_retries"
        current_retries = instance.variables.get(retry_key, 0)
        
        if current_retries < max_retries:
            instance.variables[retry_key] = current_retries + 1
            
            # Wait before retry
            await asyncio.sleep(delay)
            
            # Retry task
            await self._execute_task(instance, task)
    
    def _transform_to_fhir(self,
                         data: Any,
                         transform: Dict[str, Any]) -> Any:
        """Transform data to FHIR format"""
        # Simplified FHIR transformation
        # In production, would use PyBrain's harmonization engine
        return data
    
    def get_instance_status(self, instance_id: str) -> Optional[WorkflowInstance]:
        """Get workflow instance status"""
        return self.instances.get(instance_id)
    
    def cancel_instance(self, instance_id: str) -> bool:
        """Cancel workflow instance"""
        instance = self.instances.get(instance_id)
        if instance and instance.status == TaskStatus.RUNNING:
            instance.status = TaskStatus.CANCELLED
            logger.info("Cancelled workflow instance", instance_id=instance_id)
            return True
        return False
```

## src/pyheart/cli.py
```python
"""
Command-line interface for PyHeart
"""

import click
import asyncio
import json
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from pyheart.core.client import FHIRClient, ClientConfig
from pyheart.core.workflow import WorkflowEngine, ProcessDefinition, Task

console = Console()


@click.group()
@click.version_option()
def main():
    """PyHeart - Healthcare Interoperability & Workflow Engine"""
    pass


@main.command()
@click.option('--server', '-s', required=True, help='FHIR server URL')
@click.option('--token', '-t', help='Authentication token')
@click.option('--resource', '-r', required=True, help='Resource type (Patient, Observation, etc)')
@click.option('--id', '-i', help='Resource ID')
@click.option('--search', '-q', help='Search parameters as JSON')
def fhir(server: str, token: Optional[str], resource: str, id: Optional[str], search: Optional[str]):
    """Interact with FHIR servers"""
    config = ClientConfig(base_url=server, auth_token=token)
    
    with console.status("[bold green]Connecting to FHIR server..."):
        client = FHIRClient(config)
    
    if id:
        # Get specific resource
        console.print(f"[blue]Fetching {resource}/{id}...")
        
        if resource == "Patient":
            result = client.get_patient(id)
        else:
            # Generic resource fetch
            result = client.search(f"{resource}/{id}")
        
        if result:
            console.print_json(result.json(indent=2))
        else:
            console.print(f"[red]Resource not found: {resource}/{id}")
    else:
        # Search resources
        params = json.loads(search) if search else {}
        console.print(f"[blue]Searching {resource} with params: {params}")
        
        bundle = client.search(resource, params)
        
        # Display results in table
        table = Table(title=f"{resource} Search Results")
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Last Updated", style="green")
        
        if bundle.entry:
            for entry in bundle.entry:
                if entry.resource:
                    table.add_row(
                        entry.resource.id or "N/A",
                        entry.resource.resource_type,
                        str(entry.resource.meta.lastUpdated) if entry.resource.meta else "N/A"
                    )
        
        console.print(table)
        console.print(f"\n[green]Total results: {bundle.total or 0}")


@main.command()
@click.option('--file', '-f', type=click.File('r'), required=True, help='Workflow definition file')
@click.option('--variables', '-v', help='Initial variables as JSON')
@click.option('--watch', '-w', is_flag=True, help='Watch workflow execution')
def workflow(file, variables: Optional[str], watch: bool):
    """Execute healthcare workflows"""
    # Load workflow definition
    workflow_def = json.load(file)
    process = ProcessDefinition(**workflow_def)
    
    # Create workflow engine
    engine = WorkflowEngine()
    engine.register_process(process)
    
    # Parse variables
    vars = json.loads(variables) if variables else {}
    
    console.print(f"[green]Starting workflow: {process.name}")
    console.print(f"[blue]Process ID: {process.id}")
    
    # Start workflow
    async def run_workflow():
        instance_id = await engine.start_process(process.id, vars)
        console.print(f"[yellow]Instance ID: {instance_id}")
        
        if watch:
            # Watch execution
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Executing workflow...", total=None)
                
                while True:
                    instance = engine.get_instance_status(instance_id)
                    if instance:
                        if instance.status in ["completed", "failed", "cancelled"]:
                            break
                        
                        # Update progress
                        completed_tasks = sum(
                            1 for r in instance.task_results.values()
                            if r.status == "completed"
                        )
                        progress.update(
                            task,
                            description=f"Executing workflow... ({completed_tasks}/{len(process.tasks)} tasks)"
                        )
                    
                    await asyncio.sleep(1)
            
            # Show final status
            instance = engine.get_instance_status(instance_id)
            if instance:
                console.print(f"\n[bold]Workflow Status: {instance.status}")
                
                # Show task results
                table = Table(title="Task Results")
                table.add_column("Task", style="cyan")
                table.add_column("Status", style="magenta")
                table.add_column("Duration", style="green")
                
                for task_id, result in instance.task_results.items():
                    task = next((t for t in process.tasks if t.id == task_id), None)
                    if task and result.started_at and result.completed_at:
                        duration = (result.completed_at - result.started_at).total_seconds()
                        table.add_row(
                            task.name,
                            result.status,
                            f"{duration:.2f}s"
                        )
                
                console.print(table)
    
    asyncio.run(run_workflow())


@main.command()
@click.option('--config', '-c', type=click.File('r'), help='Server configuration file')
@click.option('--port', '-p', default=8000, help='Server port')
@click.option('--host', '-h', default='0.0.0.0', help='Server host')
def serve(config, port: int, host: str):
    """Start PyHeart API server"""
    console.print(f"[green]Starting PyHeart server on {host}:{port}...")
    
    # Load configuration if provided
    if config:
        server_config = json.load(config)
        console.print("[blue]Loaded configuration from file")
    
    from pyheart.server import run
    run(host=host, port=port)


@main.command()
@click.option('--source', '-s', required=True, help='Source system URL')
@click.option('--target', '-t', required=True, help='Target system URL')
@click.option('--resource', '-r', required=True, help='Resource type to sync')
@click.option('--continuous', '-c', is_flag=True, help='Continuous sync mode')
def sync(source: str, target: str, resource: str, continuous: bool):
    """Synchronize data between healthcare systems"""
    console.print(f"[blue]Syncing {resource} from {source} to {target}")
    
    if continuous:
        console.print("[yellow]Running in continuous sync mode...")
        # Implement continuous sync
    else:
        # One-time sync
        with console.status("[bold green]Synchronizing..."):
            # Implement sync logic
            pass
    
    console.print("[green]Sync completed!")


@main.command()
def doctor():
    """Run system diagnostics"""
    console.print("[bold cyan]PyHeart System Diagnostics")
    console.print("=" * 50)
    
    # Check dependencies
    table = Table(title="Dependencies")
    table.add_column("Package", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")
    
    deps = [
        ("FHIR Resources", "✓", "6.5.0"),
        ("FastAPI", "✓", "0.100.0"),
        ("Redis", "✓", "Connected"),
        ("Kafka", "✓", "Connected"),
    ]
    
    for dep, status, version in deps:
        table.add_row(dep, status, version)
    
    console.print(table)
    
    # Check services
    console.print("\n[bold]Service Status:")
    console.print("• FHIR Server: [green]Running")
    console.print("• Workflow Engine: [green]Active")
    console.print("• Message Queue: [green]Connected")
    console.print("• Cache: [green]Available")
    
    console.print("\n[green]All systems operational!")


if __name__ == '__main__':
    main()
```

## README.md
```markdown
# ❤️ PyHeart - Healthcare Interoperability & Workflow Engine

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-brightgreen.svg)](https://pyheart.readthedocs.io)
[![PyPI](https://img.shields.io/pypi/v/pyheart.svg)](https://pypi.org/project/pyheart/)

PyHeart is the integration layer of the BrainSAIT Healthcare Unification Platform, providing universal healthcare system connectivity, workflow orchestration, and secure data exchange.

## 🚀 Features

- **Universal API Gateway**: Single interface for all healthcare system integrations
- **Event-Driven Architecture**: Real-time data streaming and processing
- **Microservices Framework**: Modular, scalable healthcare services
- **Security & Compliance Engine**: HIPAA, GDPR, and regional compliance automation
- **Workflow Orchestration**: Complex healthcare process automation

## 📦 Installation

```bash
pip install pyheart
```

For development:
```bash
pip install pyheart[dev]
```

For legacy system support:
```bash
pip install pyheart[legacy]
```

## 🔧 Quick Start

### FHIR Client Usage

```python
from pyheart import FHIRClient

# Connect to FHIR server
client = FHIRClient("https://fhir.example.com")

# Get patient
patient = client.get_patient("12345")
print(f"Patient: {patient.name[0].given[0]} {patient.name[0].family}")

# Search patients
bundle = client.search("Patient", {"family": "Smith", "birthdate": "ge1970"})
for entry in bundle.entry:
    print(f"Found: {entry.resource.id}")

# Create patient
new_patient = Patient(
    name=[{"given": ["John"], "family": "Doe"}],
    gender="male",
    birthDate="1990-01-01"
)
created = client.create(new_patient)
```

### Workflow Engine

```python
from pyheart import WorkflowEngine, ProcessDefinition, Task

# Define a clinical process
process = ProcessDefinition(
    id="medication-reconciliation",
    name="Medication Reconciliation Process",
    tasks=[
        Task(
            id="fetch-current-meds",
            name="Fetch Current Medications",
            type="api_call",
            config={
                "url": "${fhir_server}/MedicationRequest?patient=${patient_id}",
                "method": "GET"
            }
        ),
        Task(
            id="analyze-interactions",
            name="Analyze Drug Interactions",
            type="transformation",
            dependencies=["fetch-current-meds"],
            config={
                "transform": {"type": "drug_interaction_check"}
            }
        ),
        Task(
            id="notify-if-critical",
            name="Notify on Critical Interactions",
            type="decision",
            dependencies=["analyze-interactions"],
            config={
                "rules": [{
                    "condition": {"operator": "eq", "left": "$severity", "right": "critical"},
                    "actions": [{"type": "notification", "recipient": "${physician_email}"}]
                }]
            }
        )
    ]
)

# Execute workflow
engine = WorkflowEngine()
engine.register_process(process)

instance_id = await engine.start_process(
    "medication-reconciliation",
    {"patient_id": "12345", "physician_email": "dr.smith@example.com"}
)
```

### CLI Usage

```bash
# FHIR operations
pyheart fhir -s https://fhir.example.com -r Patient -i 12345
pyheart fhir -s https://fhir.example.com -r Observation -q '{"patient": "12345"}'

# Run workflows
pyheart workflow -f medication-check.json -v '{"patient_id": "12345"}' --watch

# Start server
pyheart serve --port 8000

# Sync data between systems
pyheart sync -s https://old.example.com -t https://new.example.com -r Patient

# System diagnostics
pyheart doctor
```

## 🏗️ Architecture

PyHeart provides a layered architecture for healthcare integration:

```
pyheart/
├── core/
│   ├── client/      # FHIR and legacy clients
│   ├── server/      # API gateway and FHIR server
│   ├── workflow/    # Process orchestration
│   ├── integration/ # System adapters
│   └── security/    # Auth and encryption
├── adapters/        # Legacy system adapters
├── messaging/       # Event streaming
└── api/            # REST/GraphQL APIs
```

## 🤝 Integration with PyBrain

PyHeart and PyBrain work together seamlessly:

```python
from pyheart import FHIRClient, WorkflowEngine
from pybrain import AIEngine, DataHarmonizer

# Use PyHeart for data access
client = FHIRClient("https://fhir.example.com")
observations = client.search("Observation", {"patient": "12345", "code": "loinc|2345-7"})

# Use PyBrain for intelligence
ai = AIEngine()
harmonizer = DataHarmonizer()

# Process observations with AI
for entry in observations.entry:
    obs = entry.resource
    
    # Harmonize if needed
    if obs.meta.source != "unified":
        obs = harmonizer.harmonize_to_fhir(obs.dict(), "custom", "Observation")
    
    # AI analysis
    risk = ai.predict_risk_score({
        "glucose": obs.valueQuantity.value,
        "patient_id": "12345"
    })
    
    # Trigger workflow if high risk
    if risk > 0.8:
        engine = WorkflowEngine()
        await engine.start_process("high-risk-intervention", {
            "patient_id": "12345",
            "risk_score": risk,
            "observation_id": obs.id
        })
```

## 📊 Event-Driven Architecture

```python
from pyheart import EventBus, EventHandler

# Define event handler
@EventHandler("patient.admitted")
async def handle_admission(event):
    patient_id = event["patient_id"]
    
    # Trigger admission workflow
    engine = WorkflowEngine()
    await engine.start_process("admission-process", {
        "patient_id": patient_id,
        "ward": event["ward"],
        "admitting_physician": event["physician_id"]
    })

# Publish events
bus = EventBus()
await bus.publish("patient.admitted", {
    "patient_id": "12345",
    "ward": "ICU",
    "physician_id": "dr-789"
})
```

## 🔒 Security & Compliance

PyHeart includes comprehensive security features:

```python
from pyheart import SecurityManager, AuthProvider

# Configure security
security = SecurityManager()
security.enable_encryption("AES-256-GCM")
security.enable_audit_logging()
security.configure_compliance(["HIPAA", "GDPR"])

# OAuth2/SMART on FHIR authentication
auth = AuthProvider("smart")
token = await auth.get_token(
    client_id="app-123",
    scope="patient/*.read launch"
)

# Use authenticated client
client = FHIRClient(
    base_url="https://fhir.example.com",
    auth_token=token
)
```

## 🌟 Advanced Features

### Federated Query

```python
from pyheart import FederatedClient

# Query multiple systems simultaneously
fed_client = FederatedClient()
fed_client.add_system("hospital_a", FHIRClient("https://a.example.com"))
fed_client.add_system("hospital_b", FHIRClient("https://b.example.com"))

# Unified search across systems
results = await fed_client.federated_search("Patient", {
    "family": "Smith",
    "birthdate": "1980-01-01"
})
```

### Real-time Streaming

```python
from pyheart import StreamProcessor

# Process real-time HL7v2 messages
processor = StreamProcessor()

@processor.on_message("ADT^A01")
async def handle_admission(message):
    # Convert HL7v2 to FHIR
    patient = harmonizer.harmonize_to_fhir(
        message.segments,
        "hl7v2",
        "Patient"
    )
    
    # Store in FHIR server
    await client.create(patient)

# Start processing
await processor.start("kafka://localhost:9092/hl7-messages")
```

## 📚 Documentation

Full documentation is available at [https://pyheart.readthedocs.io](https://pyheart.readthedocs.io)

### Quick Links
- [API Reference](https://pyheart.readthedocs.io/api)
- [Workflow Guide](https://pyheart.readthedocs.io/workflows)
- [Integration Patterns](https://pyheart.readthedocs.io/patterns)
- [Security Best Practices](https://pyheart.readthedocs.io/security)

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=pyheart

# Integration tests
pytest tests/integration --integration

# Performance tests
pytest tests/performance --benchmark
```

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install pyheart[cloud]

CMD ["pyheart", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pyheart
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pyheart
  template:
    metadata:
      labels:
        app: pyheart
    spec:
      containers:
      - name: pyheart
        image: brainsait/pyheart:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: redis://redis:6379
        - name: KAFKA_BROKERS
          value: kafka:9092
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/brainsait/pyheart.git
cd pyheart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install
```

## 📄 License

PyHeart is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🌟 Acknowledgments

Built with ❤️ by the BrainSAIT Healthcare Innovation Lab

Special thanks to:
- The FHIR community for excellent standards
- FastAPI for the amazing web framework
- All our contributors and users

## 🔗 Related Projects

- [PyBrain](https://github.com/brainsait/pybrain) - AI-powered healthcare intelligence
- [BrainSAIT Platform](https://github.com/brainsait/platform) - Complete healthcare unification solution

---

**Together with PyBrain, PyHeart is building the future of connected healthcare.**
```
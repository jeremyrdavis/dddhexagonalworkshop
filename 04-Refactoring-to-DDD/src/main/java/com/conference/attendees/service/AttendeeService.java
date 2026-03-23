package com.conference.attendees.service;

import com.conference.attendees.dto.AttendeeRegistrationRequest;
import com.conference.attendees.dto.AttendeeResponse;
import com.conference.attendees.model.Address;
import com.conference.attendees.model.AttendeeEntity;
import com.conference.attendees.repository.AttendeeRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;
import java.util.stream.Collectors;

/**
 * Traditional service layer containing business logic.
 * This follows the transaction script pattern and will be
 * refactored to DDD Application Services later.
 */
@ApplicationScoped
public class AttendeeService {

    private static final Logger logger = Logger.getLogger(AttendeeService.class.getName());

    @Inject
    private AttendeeRepository attendeeRepository;

    @Inject
    private EventPublisher eventPublisher;

    public AttendeeResponse registerAttendee(AttendeeRegistrationRequest request) {
        logger.info("Registering attendee: " + request.getEmail());

        // Business validation
        validateRegistrationRequest(request);

        // Check if attendee already exists
        if (attendeeRepository.existsByEmail(request.getEmail())) {
            throw new AttendeeAlreadyExistsException(
                "Attendee with email " + request.getEmail() + " already exists");
        }

        // Create address object
        Address address = new Address(
            request.getStreetAddress(),
            request.getBus(),
            request.getPostalCode(),
            request.getTownOrMunicipality()
        );

        // Create attendee entity
        AttendeeEntity attendee = new AttendeeEntity(
            request.getEmail(),
            request.getFirstName(),
            request.getLastName(),
            address
        );

        // Save to database
        AttendeeEntity savedAttendee = attendeeRepository.save(attendee);

        // Publish event (traditional approach)
        eventPublisher.publishAttendeeRegisteredEvent(savedAttendee);

        logger.info("Successfully registered attendee: " + savedAttendee.getEmail());

        return mapToResponse(savedAttendee);
    }

    public Optional<AttendeeResponse> findAttendeeById(Long id) {
        logger.info("Finding attendee by ID: " + id);

        return attendeeRepository.findById(id)
            .map(this::mapToResponse);
    }

    public Optional<AttendeeResponse> findAttendeeByEmail(String email) {
        logger.info("Finding attendee by email: " + email);

        return attendeeRepository.findByEmail(email)
            .map(this::mapToResponse);
    }

    public List<AttendeeResponse> getAllAttendees() {
        logger.info("Getting all attendees");

        return attendeeRepository.findAll()
            .stream()
            .map(this::mapToResponse)
            .collect(Collectors.toList());
    }

    public List<AttendeeResponse> getAllAttendees(int page, int size) {
        logger.info("Getting attendees with pagination - page: " + page + ", size: " + size);

        int offset = page * size;
        return attendeeRepository.findAll(offset, size)
            .stream()
            .map(this::mapToResponse)
            .collect(Collectors.toList());
    }

    public long getTotalAttendees() {
        return attendeeRepository.count();
    }

    public AttendeeResponse updateAttendee(Long id, AttendeeRegistrationRequest request) {
        logger.info("Updating attendee with ID: " + id);

        AttendeeEntity attendee = attendeeRepository.findById(id)
            .orElseThrow(() -> new AttendeeNotFoundException("Attendee with ID " + id + " not found"));

        validateRegistrationRequest(request);

        // Update fields
        attendee.setFirstName(request.getFirstName());
        attendee.setLastName(request.getLastName());

        Address updatedAddress = new Address(
            request.getStreetAddress(),
            request.getBus(),
            request.getPostalCode(),
            request.getTownOrMunicipality()
        );
        attendee.setAddress(updatedAddress);

        AttendeeEntity updatedAttendee = attendeeRepository.save(attendee);

        logger.info("Successfully updated attendee: " + updatedAttendee.getEmail());

        return mapToResponse(updatedAttendee);
    }

    public void deleteAttendee(Long id) {
        logger.info("Deleting attendee with ID: " + id);

        if (!attendeeRepository.findById(id).isPresent()) {
            throw new AttendeeNotFoundException("Attendee with ID " + id + " not found");
        }

        attendeeRepository.deleteById(id);
        logger.info("Successfully deleted attendee with ID: " + id);
    }

    private void validateRegistrationRequest(AttendeeRegistrationRequest request) {
        if (request.getEmail() == null || request.getEmail().trim().isEmpty()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (request.getFirstName() == null || request.getFirstName().trim().isEmpty()) {
            throw new IllegalArgumentException("First name is required");
        }
        if (request.getLastName() == null || request.getLastName().trim().isEmpty()) {
            throw new IllegalArgumentException("Last name is required");
        }
        if (request.getStreetAddress() == null || request.getStreetAddress().trim().isEmpty()) {
            throw new IllegalArgumentException("Street address is required");
        }
        if (request.getPostalCode() == null || request.getPostalCode().trim().isEmpty()) {
            throw new IllegalArgumentException("Postal code is required");
        }
        if (request.getTownOrMunicipality() == null || request.getTownOrMunicipality().trim().isEmpty()) {
            throw new IllegalArgumentException("Town or municipality is required");
        }

        // Email format validation
        if (!request.getEmail().matches("^[A-Za-z0-9+_.-]+@([A-Za-z0-9.-]+\\.[A-Za-z]{2,})$")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }

    private AttendeeResponse mapToResponse(AttendeeEntity entity) {
        return new AttendeeResponse(
            entity.getId(),
            entity.getEmail(),
            entity.getFirstName(),
            entity.getLastName(),
            entity.getAddress().getStreetAddress(),
            entity.getAddress().getBus(),
            entity.getAddress().getPostalCode(),
            entity.getAddress().getTownOrMunicipality(),
            entity.getRegistrationDate(),
            entity.getStatus().toString()
        );
    }
}
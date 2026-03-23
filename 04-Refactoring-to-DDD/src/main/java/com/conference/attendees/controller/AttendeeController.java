package com.conference.attendees.controller;

import com.conference.attendees.dto.AttendeeRegistrationRequest;
import com.conference.attendees.dto.AttendeeResponse;
import com.conference.attendees.service.AttendeeAlreadyExistsException;
import com.conference.attendees.service.AttendeeNotFoundException;
import com.conference.attendees.service.AttendeeService;
import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.net.URI;
import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

/**
 * Traditional REST controller following MVC pattern.
 * This will be refactored to use hexagonal architecture later.
 */
@Path("/api/attendees")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AttendeeController {

    private static final Logger logger = Logger.getLogger(AttendeeController.class.getName());

    @Inject
    private AttendeeService attendeeService;

    @POST
    public Response registerAttendee(@Valid AttendeeRegistrationRequest request) {
        logger.info("REST: Registering attendee with email: " + request.getEmail());

        try {
            AttendeeResponse response = attendeeService.registerAttendee(request);
            logger.info("REST: Successfully registered attendee: " + response.getEmail());

            return Response.created(URI.create("/api/attendees/" + response.getId()))
                    .entity(response)
                    .build();

        } catch (AttendeeAlreadyExistsException e) {
            logger.warning("REST: Attendee already exists: " + e.getMessage());
            return Response.status(Response.Status.CONFLICT)
                    .entity(new ErrorResponse("ATTENDEE_ALREADY_EXISTS", e.getMessage()))
                    .build();

        } catch (IllegalArgumentException e) {
            logger.warning("REST: Invalid input: " + e.getMessage());
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(new ErrorResponse("INVALID_INPUT", e.getMessage()))
                    .build();

        } catch (Exception e) {
            logger.severe("REST: Unexpected error registering attendee: " + e.getMessage());
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"))
                    .build();
        }
    }

    @GET
    @Path("/{id}")
    public Response getAttendeeById(@PathParam("id") Long id) {
        logger.info("REST: Getting attendee by ID: " + id);

        Optional<AttendeeResponse> attendee = attendeeService.findAttendeeById(id);

        if (attendee.isPresent()) {
            return Response.ok(attendee.get()).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(new ErrorResponse("ATTENDEE_NOT_FOUND", "Attendee with ID " + id + " not found"))
                    .build();
        }
    }

    @GET
    @Path("/email/{email}")
    public Response getAttendeeByEmail(@PathParam("email") String email) {
        logger.info("REST: Getting attendee by email: " + email);

        Optional<AttendeeResponse> attendee = attendeeService.findAttendeeByEmail(email);

        if (attendee.isPresent()) {
            return Response.ok(attendee.get()).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(new ErrorResponse("ATTENDEE_NOT_FOUND", "Attendee with email " + email + " not found"))
                    .build();
        }
    }

    @GET
    public Response getAllAttendees(@QueryParam("page") @DefaultValue("0") int page,
                                   @QueryParam("size") @DefaultValue("20") int size) {
        logger.info("REST: Getting all attendees - page: " + page + ", size: " + size);

        List<AttendeeResponse> attendees = attendeeService.getAllAttendees(page, size);
        long total = attendeeService.getTotalAttendees();

        PaginatedResponse<AttendeeResponse> response = new PaginatedResponse<>(
            attendees, page, size, total
        );

        return Response.ok(response).build();
    }

    @PUT
    @Path("/{id}")
    public Response updateAttendee(@PathParam("id") Long id,
                                 @Valid AttendeeRegistrationRequest request) {
        logger.info("REST: Updating attendee with ID: " + id);

        try {
            AttendeeResponse response = attendeeService.updateAttendee(id, request);
            logger.info("REST: Successfully updated attendee: " + response.getEmail());
            return Response.ok(response).build();

        } catch (AttendeeNotFoundException e) {
            logger.warning("REST: Attendee not found: " + e.getMessage());
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(new ErrorResponse("ATTENDEE_NOT_FOUND", e.getMessage()))
                    .build();

        } catch (IllegalArgumentException e) {
            logger.warning("REST: Invalid input: " + e.getMessage());
            return Response.status(Response.Status.BAD_REQUEST)
                    .entity(new ErrorResponse("INVALID_INPUT", e.getMessage()))
                    .build();

        } catch (Exception e) {
            logger.severe("REST: Unexpected error updating attendee: " + e.getMessage());
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"))
                    .build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response deleteAttendee(@PathParam("id") Long id) {
        logger.info("REST: Deleting attendee with ID: " + id);

        try {
            attendeeService.deleteAttendee(id);
            logger.info("REST: Successfully deleted attendee with ID: " + id);
            return Response.noContent().build();

        } catch (AttendeeNotFoundException e) {
            logger.warning("REST: Attendee not found: " + e.getMessage());
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(new ErrorResponse("ATTENDEE_NOT_FOUND", e.getMessage()))
                    .build();

        } catch (Exception e) {
            logger.severe("REST: Unexpected error deleting attendee: " + e.getMessage());
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                    .entity(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"))
                    .build();
        }
    }

    @GET
    @Path("/health")
    public Response health() {
        return Response.ok("{\"status\":\"UP\"}").build();
    }
}